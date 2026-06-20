document.addEventListener('DOMContentLoaded', () => {
    const menuToggle = document.getElementById('menu-toggle');
    const menuClose = document.getElementById('menu-close');
    const sideMenu = document.getElementById('side-menu');
    const overlay = document.getElementById('overlay');

    const toggleMenu = (show) => {
        sideMenu.classList.toggle('active', show);
        overlay.classList.toggle('active', show);
    };

    menuToggle.addEventListener('click', () => toggleMenu(true));
    menuClose.addEventListener('click', () => toggleMenu(false));
    overlay.addEventListener('click', () => toggleMenu(false));

    const urlInput = document.getElementById('url-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const previewArea = document.getElementById('preview-area');
    const statusCard = document.getElementById('status-card');
    const successCard = document.getElementById('success-card');
    const videoTitle = document.getElementById('video-title');
    const videoThumb = document.getElementById('video-thumb');
    const platformTag = document.getElementById('platform-tag');
    const downloadLink = document.getElementById('download-link');

    let currentUrl = '';
    let autoDetectTimeout = null;

    urlInput.addEventListener('input', () => {
        const url = urlInput.value.trim();
        
        if (autoDetectTimeout) {
            clearTimeout(autoDetectTimeout);
        }
        
        if (url.startsWith('http://') || url.startsWith('https://')) {
            autoDetectTimeout = setTimeout(() => {
                analyzeVideo(url);
            }, 300);
        } else {
            previewArea.classList.add('hide');
        }
    });

    analyzeBtn.addEventListener('click', () => {
        const url = urlInput.value.trim();
        if (!url.startsWith('http')) {
            alert('Please enter a valid URL');
            return;
        }
        analyzeVideo(url);
    });

    async function analyzeVideo(url) {
        analyzeBtn.disabled = true;
        analyzeBtn.textContent = 'Analyzing...';
        
        try {
            const res = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });
            const data = await res.json();
            
            if (data.error) throw new Error(data.error);

            videoTitle.textContent = data.title;
            videoThumb.src = data.thumbnail || '/static/img/placeholder.png';
            platformTag.textContent = data.platform;
            
            previewArea.classList.remove('hide');
            successCard.classList.add('hide');
            statusCard.classList.add('hide');
            currentUrl = url;
        } catch (err) {
            alert('Error: ' + err.message);
        } finally {
            analyzeBtn.disabled = false;
            analyzeBtn.textContent = 'Analyze';
        }
    }

    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const format = btn.dataset.format;
            previewArea.classList.add('hide');
            statusCard.classList.remove('hide');
            
            document.getElementById('status-thumb').src = videoThumb.src;
            document.getElementById('status-title').textContent = videoTitle.textContent;
            document.getElementById('status-meta').textContent = 'Starting download...';

            const res = await fetch('/api/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: currentUrl, format })
            });
            const data = await res.json();
            pollStatus(data.id);
        });
    });

    async function pollStatus(id) {
        const res = await fetch(`/api/status/${id}`);
        const data = await res.json();

        const progressFill = document.getElementById('progress-fill');
        const progressPercent = document.getElementById('progress-percent');
        const statusMeta = document.getElementById('status-meta');

        if (data.status === 'starting') {
            progressFill.style.width = '5%';
            progressPercent.textContent = '5%';
            statusMeta.textContent = 'Initializing download...';
            setTimeout(() => pollStatus(id), 300);
            
        } else if (data.status === 'downloading') {
            const percent = data.progress || '0';
            progressFill.style.width = `${percent}%`;
            progressPercent.textContent = `${percent}%`;
            
            if (data.speed) {
                statusMeta.textContent = `Downloading at ${data.speed}`;
            } else {
                statusMeta.textContent = `Downloading... ${percent}%`;
            }
            setTimeout(() => pollStatus(id), 300);
            
        } else if (data.status === 'processing_files') {
            progressFill.style.width = '95%';
            progressPercent.textContent = '95%';
            statusMeta.textContent = 'Processing files...';
            setTimeout(() => pollStatus(id), 300);
            
        } else if (data.status === 'completed') {
            progressFill.style.width = '100%';
            progressPercent.textContent = '100%';
            statusMeta.textContent = 'Download Complete!';
            
            setTimeout(() => {
                statusCard.classList.add('hide');
                successCard.classList.remove('hide');
                downloadLink.href = `/file/${id}`;
                loadHistory();
            }, 500);
            
        } else if (data.status === 'error') {
            statusCard.classList.add('hide');
            alert('Download failed: ' + (data.error || 'Unknown error'));
            
        } else {
            const statusText = data.status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase());
            statusMeta.textContent = statusText + '...';
            
            const percent = data.progress || '10';
            progressFill.style.width = `${percent}%`;
            progressPercent.textContent = `${percent}%`;
            
            setTimeout(() => pollStatus(id), 500);
        }
    }

    let allHistory = [];
    let showingAll = false;

    async function loadHistory() {
        const res = await fetch('/api/history');
        const data = await res.json();
        allHistory = data;
        
        displayHistory();
    }

    function displayHistory() {
        const list = document.getElementById('history-list');
        const seeAllBtn = document.getElementById('see-all-btn');
        
        if (allHistory.length === 0) {
            list.innerHTML = '<p style="text-align:center; color:#9CA3AF; padding:40px;">No downloads yet</p>';
            if (seeAllBtn) seeAllBtn.style.display = 'none';
            return;
        }
        
        const itemsToShow = showingAll ? allHistory : allHistory.slice(0, 1);
        
        list.innerHTML = itemsToShow.map(item => {
            const fileType = item.filename && item.filename.endsWith('.mp3') ? 'Audio' : 'Video';
            
            return `
            <div class="history-item">
                <img src="${item.thumbnail || ''}" class="history-thumb">
                <div class="history-body">
                    <h5>${item.title}</h5>
                    <div class="history-meta">
                        <span>${item.platform} • ${fileType}</span>
                        <a href="/file/${item.id}" class="btn-circle">
                            <i data-lucide="download" size="16"></i>
                        </a>
                    </div>
                </div>
            </div>
        `}).join('');
        
        if (seeAllBtn) {
            if (allHistory.length > 1) {
                seeAllBtn.style.display = 'inline-block';
                seeAllBtn.textContent = showingAll ? 'Show Less' : `See All (${allHistory.length})`;
            } else {
                seeAllBtn.style.display = 'none';
            }
        }
        
        lucide.createIcons();
    }

    const seeAllBtn = document.getElementById('see-all-btn');
    if (seeAllBtn) {
        seeAllBtn.addEventListener('click', (e) => {
            e.preventDefault();
            showingAll = !showingAll;
            displayHistory();
        });
    }

    loadHistory();
    
    setInterval(loadHistory, 5000);
});
