base = "TIMOTHY".split("");
letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

const rand = (min, max) => Math.floor(Math.random() * (max - min)) + min;

const doAnimation = () => {
    text = document.getElementById('name');
    count = rand(1, 7);
    for (let i = 0; i < count; ++i) {
        base[6 - i] = letters[rand(0, 26)];
        text.innerHTML = base.join("");
    }
}

setInterval(() => {
    const animation = setInterval(doAnimation, 70);
    setTimeout(() => {
        clearInterval(animation);
        base = "TIMOTHY".split("");
        text.innerHTML = "TIMOTHY";
    }, 1000);
}, 9000);
