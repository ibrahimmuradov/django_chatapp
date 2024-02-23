function removeFriend(id){
    $.ajax({
        type: 'POST',
        url: '/remove-friend/',
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
            friendID: id
        },

        success: function(data) {
            if (data.success){
                $('#friend-' + data.success).remove()
                location.reload()
            }
        },

        error: function(xhr, errmsg, err){},

    });
}

function acceptInvite(id){
    $.ajax({
        type: 'POST',
        url: '/accept-invite/',
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
            id: id
        },

        success: function(data){
            if (data.success){
                $('#incoming-invitation-' + data.success).remove()
                location.reload()
            }
        },

        error: function(xhr, errmsg, err){},
    });
}

function denyInvite(id){
    $.ajax({
        type: 'POST',
        url: '/deny-invite/',
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
            id: id
        },

        success: function(data){
            if (data.success){
                $('#incoming-invitation-' + data.success).remove()
                location.reload()
            }
        },

        error: function(xhr, errmsg, err){},
    });
}

function cancelInvite(id){
    $.ajax({
        type: 'POST',
        url: '/cancel-invite/',
        data: {
            csrfmiddlewaretoken: csrfToken,
            action: 'post',
            id: id
        },

        success: function(data){
            if (data.success){
                $('#outgoing-invitation-' + data.success).remove();
                location.reload()
            }
        },

        error: function(xhr, errmsg, err){},
    });
}