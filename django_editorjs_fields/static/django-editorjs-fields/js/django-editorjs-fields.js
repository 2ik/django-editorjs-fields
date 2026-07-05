;(function () {
  const pluginName = "django_editorjs_fields"
  const pluginHelp =
    "Write about the issue here: https://github.com/2ik/django-editorjs-fields/issues"

  function initEditorJsPlugin() {
    const fields = document.querySelectorAll("[data-editorjs-textarea]")

    for (let i = 0; i < fields.length; i++) {
      initEditorJsField(fields[i])
    }
  }

  function initEditorJsField(textarea) {
    if (!textarea) {
      logError("bad textarea")
      return false
    }

    const id = textarea.getAttribute("id")

    if (!id) {
      logError("empty field 'id'")
      return false
    }

    const holder = document.getElementById(id + "_editorjs_holder")

    if (!holder) {
      logError("holder not found")
      return false
    }

    if (id.indexOf("__prefix__") !== -1) return

    let config
    try {
      config = JSON.parse(textarea.getAttribute("data-config"))
    } catch (error) {
      console.error(error)
      logError(
        "invalid 'data-config' on field: " + id + " . Clear the field manually"
      )
      holder.remove()
      return false
    }

    let text = textarea.value.trim()

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

    const editorConfig = {
      id,
      holder,
      data: text,
    }

    if ("tools" in config) {
      const tools = config.tools

      for (const plugin in tools) {
        const cls = tools[plugin].class

        if (cls && typeof cls === "string") {
          let ctor = window[cls]

          // Handle ESM-style exports: { default: Constructor }
          if (ctor && typeof ctor === "object" && ctor.default && typeof ctor.default === "function") {
            ctor = ctor.default
          }

          if (typeof ctor === "function") {
            tools[plugin].class = ctor
          } else {
            delete tools[plugin]
            logError("[" + plugin + "] Class " + cls + " Not Found")
          }
        }
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

    const editor = new EditorJS(editorConfig)
    holder.setAttribute("data-processed", 1)
    textarea.setAttribute("data-processed", 1)
  }

  function logError(msg) {
    console.error(pluginName + " - " + msg + ". " + pluginHelp)
  }

  addEventListener("DOMContentLoaded", initEditorJsPlugin)

  // Event — formset:added (Django 3.2+)
  if (typeof django === "object" && django.jQuery) {
    django.jQuery(document).on("formset:added", function (event, $row) {
      let areas

      if (event.detail && event.detail.$row) {
        // Django 4.1+: CustomEvent with $row in detail
        const row = event.detail.$row[0] || event.detail.$row
        areas = row.querySelectorAll("[data-editorjs-textarea]")
      } else if ($row && $row.length) {
        // Django <=4.0: jQuery event with $row as second argument
        areas = $row.find("[data-editorjs-textarea]").get()
      } else {
        // Fallback: find unprocessed textareas
        areas = event.target.querySelectorAll("[data-editorjs-textarea]:not([data-processed])")
      }

      if (areas) {
        for (let i = 0; i < areas.length; i++) {
          initEditorJsField(areas[i])
        }
      }
    })
  }
})()
