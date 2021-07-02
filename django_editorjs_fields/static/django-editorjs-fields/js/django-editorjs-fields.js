function initEditorJsField(field_id, config) {
  var pluginName = "django_editorjs_fields - " + field_id
  var pluginHelp =
    "Write about the issue here: https://github.com/2ik/django-editorjs-fields/issues"
  var textarea = document.getElementById(field_id)
  var holder = textarea.nextElementSibling
  var text = textarea.value.trim()

  if (text) {
    try {
      text = JSON.parse(text)
    } catch (error) {
      console.error(error)
      console.error(
        pluginName +
          " - invalid json data from the database. Clear the field manually. " +
          pluginHelp
      )
      holder.remove()
      return false
    }
  }

  textarea.style.display = "none" // remove old textarea

  var editorConfig = {
    id: field_id,
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
      console.error(
        pluginName +
          " - [" +
          plugin +
          "] Class " +
          cls +
          " Not Found. " +
          pluginHelp
      )
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
        textarea.value = JSON.stringify(data)
      })
      .catch(function (error) {
        console.log("save error: ", error)
      })
  }
  var editor = new EditorJS(editorConfig)
}
