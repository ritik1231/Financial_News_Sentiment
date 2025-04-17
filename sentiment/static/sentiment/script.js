function analyzeSentiment() {
    const headline = document.getElementById('headline').value;
    fetch('/predict/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ headline })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('result').innerText = `Sentiment: ${data.sentiment}`;
    });
}

function getCSRFToken() {
    const cookie = document.cookie.match(/csrftoken=([^;]+)/);
    return cookie ? cookie[1] : '';
}