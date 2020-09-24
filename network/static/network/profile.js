document.addEventListener('DOMContentLoaded', () => {

    var follow_btn = document.querySelector('#follow');
    var bio_btn = document.querySelector('#bio')

    if (follow_btn != null) {
        follow_btn.addEventListener('click', () => {
            var button = document.querySelector('#follow');
            follow_user(button);
        });
    }

    if (bio_btn != null) {
        bio_btn.addEventListener('click', () => {
            const btn = document.querySelector('#bio');
            edit_bio(btn);
        });
    }

});

function follow_user(button) {

    const id = button.dataset.userid;
    const status = button.dataset.status;
    var follow;
    if (status == "following") {
        follow = false
    } else {
        follow = true
    }

    // PUT request to follow/unfollow user
    fetch(`/followuser/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
            follow: follow
        })
    })

    var count = document.querySelector('#follower-count').innerHTML;
    if (follow) {
        count++;
        button.classList.value = "btn btn-danger";
        button.innerHTML = "Unfollow";
        button.dataset.status = "following";
    } else {
        count--;
        button.classList.value = "btn btn-info";
        button.innerHTML = "Follow";
        button.dataset.status = "notfollowing";
    }
    document.querySelector('#follower-count').innerHTML = count;
}

function edit_bio(button) {

    const id = button.dataset.userid;
    button.style.display = 'none';

    var content = document.querySelector('#bio-content').innerHTML;
    document.querySelector('#bio-content').style.display = 'none';

    var div = document.querySelector('.bio-info');

    var textarea = document.createElement('textarea');
    textarea.innerHTML = content;
    textarea.classList = "form-control mb-2";
    textarea.rows = 5;
    textarea.cols = 30;

    var submit = document.createElement('input');
    submit.type = "submit";
    submit.classList = "btn btn-primary mb-1";
    submit.value = "Save";

    div.append(textarea);
    div.append(submit);

    div.children[1].onclick = () => {

        // POST request
        content = div.children[0].value;
        fetch('/editbio', {
            method: 'POST',
            body: JSON.stringify({
                'id': id,
                'bio': content
            })
        })
            .then(response => response.json())
            .then(result => {
                console.log(result.status);
                if (result.status) {
                    button.style.display = 'block';
                    document.querySelector('#bio-content').style.display = 'block';
                    document.querySelector('#bio-content').innerHTML = content;
                    if (content == "") {
                        button.innerHTML = "Add Bio";
                    } else {
                        button.innerHTML = "Update Bio";
                    }
                    div.children[0].remove();
                    div.children[0].remove();
                } else {
                    console.log(result)
                }

            })
    }

}