let currentSound = null;

function playAudio(filename) {
    if (currentSound) {
        currentSound.stop();
    }
    document.getElementById('play-pause').textContent = "loading...";
    currentSound = new Howl({
        src: [`/audio/${filename}`],
        autoplay: false,
        onload: function() {
            currentSound.play();
            document.getElementById('duration').textContent = formatTime(currentSound.duration());
            document.getElementById('volume').value = currentSound.volume();
        },
        onplay: function() {
            console.log("onplay");
            document.getElementById('play-pause').classList.toggle('fa-play');
            requestAnimationFrame(updateProgress);
        },
        onpause: function() {
            console.log("onpause");
            document.getElementById('play-pause').classList.toggle('fa-pause');
        },
        onend: function() {
            document.getElementById('play-pause').classList.toggle('fa-pause');
            document.getElementById('progress').value = 0;
            document.getElementById('current-time').textContent = "00:00";
        },
        onseek: function() {
            requestAnimationFrame(updateProgress);
        }
    });

    document.getElementById('play-pause').addEventListener('click',
        function () {
            if (currentSound.playing()) {
                currentSound.pause();
            } else {
                currentSound.play();
            }
        });
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