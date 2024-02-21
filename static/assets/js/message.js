const csrfToken = document.getElementsByName('csrfmiddlewaretoken')[0].value;

function deleteMessage(id){
    $.ajax({
        type: "POST",
        url: '/delete-message/',
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
            messageID: id
        },

        success: function (data){
				if (data.success) {
		            var getMessageElement = document.getElementById('message-' + id);
		            getMessageElement.remove();
				}
		},

		error: function (xhr, errmsg, err) {},
    });
}

function copyMessage(id){
    getMessage = document.querySelector('#message-text-' + id);
    navigator.clipboard.writeText(getMessage.innerText)

    getCopyElement = document.querySelector('#copy-message-' + id);
    getCopyElement.innerHTML = `Copied <i class="ri-check-line float-end text-muted"></i>`
}
