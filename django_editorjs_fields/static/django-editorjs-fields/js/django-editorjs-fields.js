function initEditorJsField(field_id, config) {
  console.log(config)
  const pluginName = "django_editorjs_fields"
  const pluginHelp =
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
  // remove old textarea
  textarea.style.display = "none"

  // config
  var editorConfig = {
    holder: holder,
    data: text,
  }

  // set config
  if ("tools" in config) {
    var tools = config.tools

    for (const plugin in tools) {
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
    editorConfig.hideToolbar = config.inlineToolbar
  }

  if ("minHeight" in config) {
    editorConfig.minHeight = config.minHeight || 300
  }

  if ("logLevel" in config) {
    editorConfig.logLevel = config.logLevel || "VERBOSE"
  }

  if ("placeholder" in config) {
    editorConfig.placeholder = config.placeholder || "Type text..."
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
    editorConfig.i18n = config.i18n || false
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
  console.log(editorConfig)
  const editor = new EditorJS(editorConfig)
}
