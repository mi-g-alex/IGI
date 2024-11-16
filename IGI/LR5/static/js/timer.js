function startCountdown(div, duration = 24 * 60 * 60 * 1000) {
    let endTime = localStorage.getItem('endTime');

    if (!endTime) {
        endTime = Date.now() + duration;
        localStorage.setItem('endTime', endTime);
    }

    const interval = setInterval(() => {
        const now = Date.now();
        const remainingTime = endTime - now;

        if (remainingTime <= 0) {
            document.getElementById('countdown').textContent = 'Время вышло!';
            localStorage.removeItem('endTime');
            clearInterval(interval);
        } else {
            const hours = Math.floor((remainingTime / (1000 * 60 * 60)))
            const minutes = Math.floor((remainingTime % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((remainingTime % (1000 * 60)) / 1000);

            div.textContent = `Remain: ${hours}h ${minutes}m ${seconds}s`;
        }
    }, 1000);
}