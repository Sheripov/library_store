async function renderComments(book_id) {
    async function getComments(book_id) {
        let url = '/api/book_comments/?user_id=&book_id='+ book_id;
        try {
            let res = await fetch(url);
            return await res.json();
        } catch (error) {
            console.log(error);
        }
    }
    let comments = await getComments(book_id);
    let html = '';
    comments.map(comment => {
    let htmlSegment = `<li class="media">
                            <div class="alert alert-dismissible alert-secondary">
                                    <h6 class="media-heading text-uppercase reviews">${comment.user}</h6>
                                    <p class="media-comment">${comment.comment}</p>
                            </div>
                    </li>`;
    html += htmlSegment;
    });
    let container = document.querySelector('.comments');
    container.innerHTML = html;
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


async function postData(url = '', data = {}) {
  const response = await fetch(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie("csrftoken"),
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: JSON.stringify(data)
  });
  return await response.json();
}


async function myComment() {
    const comment = document.getElementById("comment").value;
    const book_id = document.getElementById("book_id").value;
    const user_id = document.getElementById("user_id").value;
    const post_url = document.getElementById("post_url").value;
    let data = {
        'comment': comment,
        'book': book_id,
        'user': user_id,
    };
    await postData(post_url, data);
    await renderComments(book_id);
}