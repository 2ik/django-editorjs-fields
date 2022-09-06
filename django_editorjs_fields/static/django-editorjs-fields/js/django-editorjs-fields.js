;(function () {
  var pluginName = "django_editorjs_fields"
  var pluginHelp =
    "Write about the issue here: https://github.com/2ik/django-editorjs-fields/issues"

  function initEditorJsPlugin() {
    var fields = document.querySelectorAll("[data-editorjs-textarea]")

    for (let i = 0; i < fields.length; i++) {
      initEditorJsField(fields[i])
    }
  }

  function initEditorJsField(textarea) {
    if (!textarea) {
      logError("bad textarea")
      return false
    }

    var id = textarea.getAttribute("id")

    if (!id) {
      logError("empty field 'id'")
      holder.remove()
      return false
    }

    var holder = document.getElementById(id + "_editorjs_holder")

    if (!holder) {
      logError("holder not found")
      holder.remove()
      return false
    }

    if (id.indexOf("__prefix__") !== -1) return

    try {
      var config = JSON.parse(textarea.getAttribute("data-config"))
    } catch (error) {
      console.error(error)
      logError(
        "invalid 'data-config' on field: " + id + " . Clear the field manually"
      )
      holder.remove()
      return false
    }

    var text = textarea.value.trim()

    if (text) {
      try {
        text = JSON.parse(text)
      } catch (error) {
        console.error(error)
        logError(
          "invalid json data from the database. Clear the field manually"
        )
        holder.remove()
        return false
      }
    }

    textarea.style.display = "none" // remove old textarea

    var editorConfig = {
      id: id,
      holder: holder,
      data: text,
    }

    if ("tools" in config) {
      // set config
      var tools = config.tools

      for (var plugin in tools) {
        var cls = tools[plugin].class

        if (cls && window[cls] != undefined) {
          tools[plugin].class = eval(cls)
          continue
        }

        delete tools[plugin]
        logError("[" + plugin + "] Class " + cls + " Not Found")
      }

      editorConfig.tools = tools
    }

    if ("autofocus" in config) {
      editorConfig.autofocus = !!config.autofocus
    }

    if ("hideToolbar" in config) {
      editorConfig.hideToolbar = !!config.hideToolbar
    }

    if ("inlineToolbar" in config) {
      editorConfig.inlineToolbar = config.inlineToolbar
    }

    if ("readOnly" in config) {
      editorConfig.readOnly = config.readOnly
    }

    if ("minHeight" in config) {
      editorConfig.minHeight = config.minHeight || 300
    }

    if ("logLevel" in config) {
      editorConfig.logLevel = config.logLevel || "VERBOSE"
    } else {
      editorConfig.logLevel = "ERROR"
    }

    if ("placeholder" in config) {
      editorConfig.placeholder = config.placeholder || "Type text..."
    } else {
      editorConfig.placeholder = "Type text..."
    }

    if ("defaultBlock" in config) {
      editorConfig.defaultBlock = config.defaultBlock || "paragraph"
    }

    if ("sanitizer" in config) {
      editorConfig.sanitizer = config.sanitizer || {
        p: true,
        b: true,
        a: true,
      }
    }

    if ("i18n" in config) {
      editorConfig.i18n = config.i18n || {}
    }

    editorConfig.onChange = function () {
      editor
        .save()
        .then(function (data) {
          if (data.blocks.length) {
            textarea.value = JSON.stringify(data)
          } else {
            textarea.value = 'null'
          }
        })
        .catch(function (error) {
          console.log("save error: ", error)
        })
    }
    var editor = new EditorJS(editorConfig)
    holder.setAttribute("data-processed", 1)
  }

  function logError(msg) {
    console.error(pluginName + " - " + msg + ". " + pluginHelp)
  }

  addEventListener("DOMContentLoaded", initEditorJsPlugin)

  // Event
  if (typeof django === "object" && django.jQuery) {
    django.jQuery(document).on("formset:added", function (event, $row) {
      var areas = $row.find("[data-editorjs-textarea]").get()

      if (areas) {
        for (let i = 0; i < areas.length; i++) {
          initEditorJsField(areas[i])
        }
      }
    })
  }
})()
