const animationController = document.querySelector('#animation-controller');

function playAnimation(className) {
    animationController.classList.remove('is-spinning', 'is-launching');
    animationController.classList.remove(className);
    void animationController.offsetWidth;
    animationController.classList.add(className);
}

animationController.addEventListener('pointerenter', () => {
    animationController.classList.add('is-hovering');
});

animationController.addEventListener('pointerleave', () => {
    animationController.classList.remove('is-hovering');
});

animationController.addEventListener('click', () => {
    playAnimation('is-spinning');
});

animationController.addEventListener('keydown', (event) => {
    if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        playAnimation('is-launching');
    }
});