document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll('.like button').forEach((button) => {
        button.onclick = () => {
            like_post(button);
        }
    });

    document.querySelectorAll('.edit-btn').forEach((button) => {
        button.onclick = () => {
            edit_post(button);
        }
    });

});

function like_post(button) {

    const id = button.dataset.postid;
    const status = button.dataset.status;
    var liked;
    if (status == "liked") {
        liked = false;
    } else {
        liked = true;
    }

    // PUT request to like post
    fetch(`/post/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            liked: liked
        })
    })
    var count = document.getElementById(`${id}-count`).innerHTML;
    var img;
    if (liked) {
        count++;
        img = "/media/like_red.png";
        button.dataset.status = "liked";
    } else {
        count--;
        img = "/media/like.png";
        button.dataset.status = "unliked"
    }
    document.getElementById(`${id}-count`).innerHTML = count;
    document.getElementById(`${id}-img`).src = img;
    return false;
}

function edit_post(button) {

    const id = button.dataset.postid;
    button.style.display = 'none';

    // GET request to get contents of post
    fetch(`/post/${id}`)
        .then(response => response.json())
        .then(post => {
            console.log(post)
            var content = post.content;

            var div = document.getElementById(`${id}post-content`);
            var textarea = document.createElement('textarea');
            textarea.innerHTML = content;
            textarea.classList = "form-control mb-1";
            textarea.rows = 5;

            var submit = document.createElement('input');
            submit.type = "submit";
            submit.classList = "btn btn-primary mb-1";
            submit.value = "Save";


            div.children[0].style.display = 'none';
            div.append(textarea);
            div.append(submit);

            div.children[2].onclick = () => {
                // POST request
                content = div.children[1].value;
                fetch('/posts', {
                    method: 'POST',
                    body: JSON.stringify({
                        'id': id,
                        'content': content
                    })
                })
                    .then(response => response.json())
                    .then(result => {
                        console.log(result.status)
                        if (result.status == 201) {
                            button.style.display = "inline-block";
                            div.children[0].style.display = "block";
                            div.children[0].innerHTML = content;
                            div.children[1].remove();
                            div.children[1].remove();
                            document.getElementById(`${id}edit-status`).children[0].innerHTML = "&nbsp;&nbsp;&nbsp;EDITED";
                        } else {
                            console.log(result);
                        }

                    });

            }

        })

}