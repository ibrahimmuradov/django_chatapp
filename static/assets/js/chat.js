const room_code = JSON.parse(document.getElementById('room_code').textContent);
const user = JSON.parse(document.getElementById('user').textContent);

const chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/' + room_code + '/');

const messages_area = document.querySelector('#messages-area');
const inputContainer = document.querySelector('#input-container');
const messageInput = document.querySelector('#chat-message-input')
const fileName = document.querySelector('#file-name')
const messageSubmitButton = document.querySelector('#chat-message-submit')
const fileInput = document.querySelector('#data-file');

const fileBtn = document.querySelector('#file-btn');

inputContainerHtml = inputContainer.innerHTML;
messageInputStyle = messageInput.style.display;
fileBtnHtml = fileBtn.innerHTML;

let file;
let file_name;
let file_type;
let file_size;


function updateInputContainer() {
    if (file) {
        messageInput.style.display = 'none';
        fileName.innerHTML = `Your file: <strong>${file.name}</strong>`;
        fileBtn.innerHTML = `<button type="button" onclick="deleteFile()" class="btn btn-link text-decoration-none font-size-16 btn-lg waves-effect">
                                <i style="color: red" class="ri-close-line"></i>
                            </button>`;
    } else {
        messageInput.style.display = messageInputStyle;
        fileName.innerHTML = '';
        fileBtn.innerHTML = fileBtnHtml;
    }
}

function chooseFileBtn(){
    fileInput.click()
    fileInput.addEventListener('change', chooseFile, false);
}

function chooseFile(event) {
    file = fileInput.files[0];
    updateInputContainer();
}

function deleteFile() {
    file = '';
    fileInput.value = '';
    updateInputContainer();
}


chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    if (data.error_type === "websocket.close"){
        alert(data.error_code + ' : ' + data.error_message);

    } else {

        var addMessage = `<li id="message-${data.data_id}" class="right">
                                <div class="conversation-list">
                                    <div class="chat-avatar">
                                        <img src="${data.user_profile_photo}" alt="">
                                    </div>
                                    <div class="user-chat-content">
                                        <div class="ctext-wrap">
                                            <div class="ctext-wrap-content">
                                                <p id="data-content" class="mb-0">

                                                 <span id="message-text-${data.data_id}">${data.message}</span>

                                                 <video id="video-${data.data_id}" width="250" controls>
                                                    <source src="${data.file}">
                                                 </video>

                                                  <audio id="audio-${data.data_id}" style='width: 250px' controls>
                                                      <source src="${data.file}">
                                                  </audio>

                                                   <div id="file-${data.data_id}" class="card p-2 mb-2">
                                                        <div class="d-flex flex-wrap align-items-center attached-file">
                                                            <div class="avatar-sm me-3 ms-0 attached-file-avatar">
                                                                <div class="avatar-title bg-primary-subtle text-primary rounded font-size-20">
                                                                    <i class="ri-file-text-fill"></i>
                                                                </div>
                                                            </div>
                                                            <div class="flex-grow-1 overflow-hidden">
                                                                <div class="text-start">
                                                                    <h5 class="font-size-14 text-truncate mb-1">
                                                                        ${data.file_name + '.' + data.file_type}</h5>
                                                                    <p class="text-muted text-truncate font-size-13 mb-0">
                                                                        ${data.file_size} MB</p>
                                                                </div>
                                                            </div>
                                                            <div class="ms-4 me-0">
                                                                <div class="d-flex gap-2 font-size-20 d-flex align-items-start">
                                                                    <div>
                                                                        <a download="${data.file_name}" href="${data.file}" class="fw-medium">
                                                                            <i class="ri-download-2-line"></i>
                                                                        </a>
                                                                    </div>
                                                                        <div id='file-delete-${data.data_id}' class="dropdown">
                                                                            <a class="dropdown-toggle text-muted" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                                                <i class="ri-more-fill"></i>
                                                                            </a>
                                                                            <div class="dropdown-menu dropdown-menu-end">
                                                                                <span class="dropdown-item" onclick="deleteMessage(${data.data_id})">Delete <i class="ri-delete-bin-line float-end text-muted"></i></span>
                                                                            </div>
                                                                        </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>

                                                <div id="photo-${data.data_id}" class="ctext-wrap">
                                                    <div class="ctext-wrap-content">
                                                        <p class="mb-0">
                                                            <ul class="list-inline message-img  mb-0">
                                                                <li class="list-inline-item message-img-list me-2 ms-0">
                                                                    <div>
                                                                        <a class="popup-img d-inline-block m-1" href="${data.file}" title="${data.file_name}">
                                                                            <img src="${data.file}" alt="" class="rounded border">
                                                                        </a>
                                                                    </div>
                                                                    <div class="message-img-link">
                                                                        <ul class="list-inline mb-0">
                                                                            <li class="list-inline-item">
                                                                                <a download="${data.file_name}" href="${data.file}" class="fw-medium">
                                                                                    <i class="ri-download-2-line"></i>
                                                                                </a>
                                                                            </li>
                                                                            <li id='photo-delete-${data.data_id}' class="list-inline-item dropdown">
                                                                                <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                                                    <i class="ri-more-fill"></i>
                                                                                </a>
                                                                                <div class="dropdown-menu">
                                                                                    <span class="dropdown-item" onclick="deleteMessage(${data.message_id})">Delete <i class="ri-delete-bin-line float-end text-muted"></i></span>
                                                                                </div>
                                                                            </li>
                                                                        </ul>
                                                                    </div>
                                                                </li>
                                                            </ul>
                                                        </p>
                                                    </div>
                                                </div>

                                                <p id="message-time-${data.data_id}" class="chat-time mb-0"><i class="ri-time-line align-middle"></i> <span class="align-middle">${data.time}</span></p>
                                            </div>
                                            <div id="message-dropdown-${data.data_id}" class="dropdown align-self-start">
                                                <a class="dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                                    <i class="ri-more-2-fill"></i>
                                                </a>
                                                <div class="dropdown-menu">
                                                    <span class="dropdown-item" id="copy-message-${data.data_id}" onclick="copyMessage(${data.data_id})">Copy <i class="ri-file-copy-line float-end text-muted"></i></span>
                                                    <span class="dropdown-item" id='message-delete-${data.data_id}' onclick="deleteMessage(${data.data_id})">Delete <i class="ri-delete-bin-line float-end text-muted"></i></span>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="conversation-name">${data.user}</div>
                                    </div>
                                </div>
                            </li>`;

        messages_area.innerHTML += addMessage;

        document.querySelector('#message-' + data.data_id).style.display = "none";
        document.querySelector('#message-text-' + data.data_id).style.display = "none";
        document.querySelector('#video-' + data.data_id).style.display = "none";
        document.querySelector('#audio-' + data.data_id).style.display = "none";
        document.querySelector('#file-' + data.data_id).style.display = "none";
        document.querySelector('#photo-' + data.data_id).style.display = "none";
        document.querySelector('#message-dropdown-' + data.data_id).style.display = "none";
        document.querySelector('#message-time-' + data.data_id).style.display = "none";

        if (data.file){
            document.querySelector('#message-' + data.data_id).style.display = "block";

            let file_types = ['pdf', 'zip', 'rar', 'txt', 'doc', 'docx', 'rtf', 'xls', 'xlsx', 'ppt', 'pptx'];
            let checkType = file_types.includes(data.file_type);

            if (checkType) {
                document.querySelector('#file-' + data.data_id).style.display = "block";
                document.querySelector('#message-time-' + data.data_id).style.display = "block";
            } else if (data.file_type == "mp4" || data.file_type == "avi" || data.file_type == "mkv" || data.file_type == "mov"){
                document.querySelector('#video-' + data.data_id).style.display = "block";
            } else if (data.file_type == "mp3" || data.file_type == "mpeg" || data.file_type == "oog") {
                document.querySelector('#audio-' + data.data_id).style.display = "block";
            } else if (data.file_type == "jpeg" || data.file_type == "png" || data.file_type == "jpg" || data.file_type == "gif") {
                document.querySelector('#photo-' + data.data_id).style.display = "block";
            }

        } else {
            document.querySelector('#message-' + data.data_id).style.display = "block";

            document.querySelector('#message-text-' + data.data_id).style.display = "block";
            document.querySelector('#message-dropdown-' + data.data_id).style.display = "block";
            document.querySelector('#message-time-' + data.data_id).style.display = "block";
        }

        if (data.user == user){
            document.querySelector('#message-' + data.data_id).setAttribute("class", "right");
        } else {
            document.querySelector('#message-' + data.data_id).setAttribute("class", "");
            document.querySelector('#message-delete-' + data.data_id).style.display = "none";
            document.querySelector('#file-delete-' + data.data_id).style.display = "none";
            document.querySelector('#photo-delete-' + data.data_id).style.display = "none";
        }

    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

messageInput.focus();
messageInput.onkeyup = function(e) {
    if (e.key === 'Enter') {
        messageSubmitButton.click();
    }
};

messageSubmitButton.onclick = function(e) {
    const message = messageInput.value;

    if (file) {
        fileType = file.type
        var type = fileType.split('/')[1]

        sizeToMmb = file.size/(1024*1024)
        roundSize = sizeToMmb.toFixed(1)

        getFileName = file.name

        var reader = new FileReader();

        reader.onload = () => {
            const fileData = reader.result.split(',')[1];

            chatSocket.send(JSON.stringify({
                'message': message,
                'user': user,
                'file': fileData,
                'file_name': getFileName.substr(0, getFileName.lastIndexOf('.')),
                'file_type': type,
                'file_size': roundSize
            }));
        };

        reader.readAsDataURL(file);

        deleteFile();
    } else {
        chatSocket.send(JSON.stringify({
            'message': message,
            'user': user
        }));

        messageInput.value = '';
    }
};