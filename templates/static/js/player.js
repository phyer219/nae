let currentSound = null;

function playAudio(filename, title) {
    console.log('================', filename)
    if (currentSound) {
        currentSound.stop();
    }
    document.getElementById('track-info').textContent = "loading...";
    currentSound = new Howl({
        src: [`/audio/${filename}`],
        autoplay: false,
        onload: function() {
            currentSound.play();
            document.getElementById('duration').textContent = formatTime(currentSound.duration());
            document.getElementById('volume').value = currentSound.volume();
            document.getElementById('track-info').textContent = title;
        },
        onplay: function() {
            console.log("onplay");
            console.log(`/audio/${filename}`);
            document.getElementById('play-pause').classList.replace(
                'fa-play', 'fa-pause');
            requestAnimationFrame(updateProgress);
        },
        onpause: function() {
            console.log("onpause");
            console.log(`/audio/${filename}`);
            document.getElementById('play-pause').classList.replace(
                'fa-pause', 'fa-play');
        },
        onend: function() {
            document.getElementById('play-pause').classList.replace(
                'fa-pause', 'fa-play');
            document.getElementById('progress').value = 0;
            document.getElementById('current-time').textContent = "00:00";
        },
        onseek: function() {
            requestAnimationFrame(updateProgress);
        }
    });


    function removeAllEventListeners(element) {
        const newElement = element.cloneNode(true);
        element.replaceWith(newElement);
        return newElement;
    }
    const playPauseButtonOld = document.getElementById('play-pause');
    const playPauseButton = removeAllEventListeners(playPauseButtonOld);

    playPauseButton.addEventListener('click',
        function () {
            if (currentSound.playing()) {
                console.log("playing........");
                currentSound.pause();
            } else {
                console.log("pausing........");
                currentSound.play();
            }
        }
    );

    document.getElementById('volume').oninput = function() {
        if (currentSound) {
            currentSound.volume(parseFloat(this.value));
        }
    };
    document.getElementById('progress').oninput = function() {
        if (currentSound) {
            currentSound.seek(parseFloat(this.value) / 100 * currentSound.duration());
        }
    };

    function updateProgress() {
        if (currentSound) {
            document.getElementById('progress').value = currentSound.seek() / currentSound.duration() * 100;
            document.getElementById('current-time').textContent = formatTime(currentSound.seek());
            if (currentSound.playing()) {
                requestAnimationFrame(updateProgress);
            }
        }
    };
};
function formatTime(seconds) {
        seconds = Math.round(seconds);

        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    };
