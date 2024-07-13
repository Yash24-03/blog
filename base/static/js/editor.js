const blogTitleField = document.querySelector('.title');
const articleField = document.querySelector('.article');

// banner
const bannerImage = document.querySelector('#banner-upload');
const banner = document.querySelector(".banner");
let bannerPath;

const publishBtn = document.querySelector('.publish-btn');
const uploadInput = document.querySelector('#image-upload');

bannerImage.addEventListener('change', () => {
    uploadImage(bannerImage, "banner");
})

uploadInput.addEventListener('change', () => {
    uploadImage(uploadInput, "image");
})

const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

const uploadImage = (uploadFile, uploadType) => {
    const [file] = uploadFile.files;
    if(file && file.type.includes("image")){
        const formData = new FormData();
        formData.append('image', file);

        fetch('/upload-image/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            body: formData
        }).then(res => res.json())
        .then(data => {
            if(uploadType == "image"){
                addImage(data.image_url, file.name);
            } else {
                bannerPath = `${location.origin}/${data.image_url}`;
                banner.style.backgroundImage = `url("${bannerPath}")`;
            }
        }).catch((err) => {
            console.error(err);
        });
    } else {
        alert("upload Image only");
    }
}

const addImage = (imagePath, alt) => {
    let curPos = articleField.selectionStart;
    let textToInsert = `\r![${alt}](${imagePath})\r`;
    articleField.value = articleField.value.slice(0, curPos) + textToInsert + articleField.value.slice(curPos);
}

publishBtn.addEventListener('click', () => {
    if(articleField.value.length && blogTitleField.value.length){
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/create-post/';
        
        const titleField = document.createElement('input');
        titleField.type = 'hidden';
        titleField.name = 'title';
        titleField.value = blogTitleField.value;
        
        const contentField = document.createElement('textarea');
        contentField.name = 'content';
        contentField.value = articleField.value;
        
        const bannerField = document.createElement('input');
        bannerField.type = 'hidden';
        bannerField.name = 'banner_image';
        bannerField.value = bannerPath;
        
        form.appendChild(titleField);
        form.appendChild(contentField);
        form.appendChild(bannerField);

        const csrfField = document.createElement('input');
        csrfField.type = 'hidden';
        csrfField.name = 'csrfmiddlewaretoken';
        csrfField.value = csrftoken;
        
        form.appendChild(csrfField);
        
        document.body.appendChild(form);
        form.submit();
    }
});
