function initEditorJsField(field_id, tools) {
    var textarea = document.getElementById(field_id)
    var holder = textarea.nextElementSibling

    var data = textarea.value.trim()

    if (data) {
        try {
            data = JSON.parse(data)
        } catch (error) {
            console.log(error)
            holder.remove()
            return false
        }
    }

    textarea.style.display = "none"

    if (tools) {
        for (const plugin in tools) {
            var cls = tools[plugin].class
            if (cls && window[cls] != undefined) {
                tools[plugin].class = eval(cls)
            }
        }
    }

    const editor = new EditorJS({
        autofocus: true,
        holder: holder,
        tools: tools || {},
        data: data || undefined,
        onChange: function () {
            editor
                .save()
                .then(function (data) {
                    textarea.value = JSON.stringify(data)
                })
                .catch(function (error) {
                    console.log("save error: ", error)
                })
        },
    })
}
