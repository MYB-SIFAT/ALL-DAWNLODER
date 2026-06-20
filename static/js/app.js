document.addEventListener('DOMContentLoaded', () => {

    const urlInput = document.getElementById('url-input');
    const analyzeBtn = document.getElementById('analyze-btn');
    const clearBtn = document.getElementById('clear-btn');
    const previewArea = document.getElementById('preview-area');
    const statusCard = document.getElementById('status-card');
    const successCard = document.getElementById('success-card');
    const videoTitle = document.getElementById('video-title');
    const videoThumb = document.getElementById('video-thumb');
    const platformTag = document.getElementById('platform-tag');
    const downloadLink = document.getElementById('download-link');
    const newDownloadBtn = document.getElementById('new-download-btn');

    let currentUrl = '';
    let autoDetectTimeout = null;
    let isAnalyzing = false;

    urlInput.addEventListener('input', () => {
        const url = urlInput.value.trim();
        clearBtn.classList.toggle('hide', !url);

        if (autoDetectTimeout) clearTimeout(autoDetectTimeout);

        if (url.startsWith('http://') || url.startsWith('https://')) {
            autoDetectTimeout = setTimeout(() => analyzeVideo(url), 400);
        } else {
            previewArea.classList.add('hide');
        }
    });

    clearBtn.addEventListener('click', () => {
        urlInput.value = '';
        clearBtn.classList.add('hide');
        previewArea.classList.add('hide');
        statusCard.classList.add('hide');
        successCard.classList.add('hide');
        currentUrl = '';
        urlInput.focus();
    });

    analyzeBtn.addEventListener('click', () => {
        const url = urlInput.value.trim();
        if (!url.startsWith('http')) {
            shakeInput();
            return;
        }
        analyzeVideo(url);
    });

    urlInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') analyzeBtn.click();
    });

    async function analyzeVideo(url) {
        if (isAnalyzing) return;
        isAnalyzing = true;
        analyzeBtn.disabled = true;
        analyzeBtn.innerHTML = '<i data-lucide="loader-2" class="spin"></i> Analyzing...';
        lucide.createIcons();

        try {
            const res = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });
            const data = await res.json();
            if (data.error) throw new Error(data.error);

            videoTitle.textContent = data.title;
            videoThumb.src = data.thumbnail || '';
            platformTag.textContent = data.platform;

            previewArea.classList.remove('hide');
            successCard.classList.add('hide');
            statusCard.classList.add('hide');
            currentUrl = url;
        } catch (err) {
            showToast('❌ ' + err.message, 'error');
        } finally {
            isAnalyzing = false;
            analyzeBtn.disabled = false;
            analyzeBtn.innerHTML = '<i data-lucide="search"></i> Analyze';
            lucide.createIcons();
        }
    }

    document.querySelectorAll('.format-btn').forEach(btn => {
        btn.addEventListener('click', async () => {
            const format = btn.dataset.format;

            previewArea.classList.add('hide');
            statusCard.classList.remove('hide');
            successCard.classList.add('hide');

            document.getElementById('status-thumb').src = videoThumb.src;
            document.getElementById('status-title').textContent = videoTitle.textContent;
            document.getElementById('status-meta').textContent = 'Starting download...';
            document.getElementById('progress-fill').style.width = '0%';
            document.getElementById('progress-percent').textContent = '0%';

            try {
                const res = await fetch('/api/download', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ url: currentUrl, format })
                });
                const data = await res.json();
                pollStatus(data.id);
            } catch (err) {
                statusCard.classList.add('hide');
                showToast('❌ Failed to start download', 'error');
            }
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
            const percent = parseFloat(data.progress) || 0;
            progressFill.style.width = `${percent}%`;
            progressPercent.textContent = `${Math.round(percent)}%`;
            statusMeta.textContent = data.speed ? `Downloading at ${data.speed}` : `Downloading... ${Math.round(percent)}%`;
            setTimeout(() => pollStatus(id), 300);

        } else if (data.status === 'processing_files') {
            progressFill.style.width = '95%';
            progressPercent.textContent = '95%';
            statusMeta.textContent = 'Processing & converting...';
            setTimeout(() => pollStatus(id), 300);

        } else if (data.status === 'completed') {
            progressFill.style.width = '100%';
            progressPercent.textContent = '100%';
            statusMeta.textContent = 'Complete!';

            setTimeout(() => {
                statusCard.classList.add('hide');
                successCard.classList.remove('hide');
                downloadLink.href = `/file/${id}`;
                lucide.createIcons();
                loadHistory();
            }, 600);

        } else if (data.status === 'error') {
            statusCard.classList.add('hide');
            showToast('❌ ' + (data.error || 'Download failed'), 'error');

        } else {
            statusMeta.textContent = data.status.replace(/_/g, ' ') + '...';
            setTimeout(() => pollStatus(id), 500);
        }
    }

    if (newDownloadBtn) {
        newDownloadBtn.addEventListener('click', () => {
            successCard.classList.add('hide');
            urlInput.value = '';
            clearBtn.classList.add('hide');
            currentUrl = '';
            urlInput.focus();
        });
    }

    let allHistory = [];
    let showingAll = false;

    async function loadHistory() {
        try {
            const res = await fetch('/api/history');
            allHistory = await res.json();
            displayHistory();
        } catch (e) { }
    }

    function formatDate(dateStr) {
        if (!dateStr) return '';
        try {
            const d = new Date(dateStr);
            return d.toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' });
        } catch { return ''; }
    }

    function displayHistory() {
        const list = document.getElementById('history-list');
        const seeAllBtn = document.getElementById('see-all-btn');

        if (allHistory.length === 0) {
            list.innerHTML = `
                <div style="grid-column:1/-1;text-align:center;padding:60px 20px;color:var(--secondary);">
                    <div style="font-size:48px;margin-bottom:12px;">📂</div>
                    <p style="font-weight:600;font-size:15px;">No downloads yet</p>
                    <p style="font-size:13px;margin-top:4px;">Your download history will appear here</p>
                </div>`;
            if (seeAllBtn) seeAllBtn.style.display = 'none';
            return;
        }

        const items = showingAll ? allHistory : allHistory.slice(0, 3);

        list.innerHTML = items.map(item => {
            const fileType = item.filename && item.filename.endsWith('.mp3') ? 'Audio' : 'Video';
            const thumbSrc = escHtml(item.thumbnail || '');
            const date = formatDate(item.date);
            const id = escHtml(item.id);
            return `
            <div class="history-item">
                <img src="${thumbSrc}" class="history-thumb" onerror="this.style.background='#f4f4f5';this.src='';this.style.height='80px'">
                <div class="history-body">
                    <div class="history-meta-top">
                        <span class="history-platform-tag">${escHtml(item.platform || 'Media')}</span>
                        <span class="history-type-tag">${escHtml(fileType)}</span>
                    </div>
                    <h5>${escHtml(item.title || 'Unknown Title')}</h5>
                    <div class="history-footer">
                        <span class="history-date">${escHtml(date)}</span>
                        <a href="/file/${id}" class="btn-circle" title="Download again">
                            <i data-lucide="download" style="width:15px;height:15px;"></i>
                        </a>
                    </div>
                </div>
            </div>`;
        }).join('');

        if (seeAllBtn) {
            if (allHistory.length > 3) {
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
    setInterval(loadHistory, 6000);

    function escHtml(str) {
        return String(str || '')
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#39;');
    }

    function shakeInput() {
        const card = document.querySelector('.main-card');
        card.style.animation = 'none';
        card.offsetHeight;
        card.style.animation = 'shake 0.4s ease';
        setTimeout(() => card.style.animation = '', 400);
    }

    function showToast(msg, type = 'info') {
        const existing = document.getElementById('toast');
        if (existing) existing.remove();

        const toast = document.createElement('div');
        toast.id = 'toast';
        toast.textContent = msg;
        toast.style.cssText = `
            position:fixed;bottom:24px;right:24px;z-index:9999;
            background:${type === 'error' ? '#1a1a1a' : '#10B981'};
            color:white;padding:14px 20px;border-radius:12px;
            font-weight:700;font-size:14px;font-family:inherit;
            box-shadow:0 8px 24px rgba(0,0,0,0.2);
            animation:slideInToast 0.3s ease;
            max-width:360px;
        `;
        document.body.appendChild(toast);
        setTimeout(() => { if (toast.parentNode) toast.remove(); }, 4000);
    }
});

const extraCSS = document.createElement('style');
extraCSS.textContent = `
    @keyframes shake {
        0%,100%{transform:translateX(0)}
        20%{transform:translateX(-6px)}
        40%{transform:translateX(6px)}
        60%{transform:translateX(-4px)}
        80%{transform:translateX(4px)}
    }
    @keyframes slideInToast {
        from{transform:translateY(20px);opacity:0}
        to{transform:translateY(0);opacity:1}
    }
    .spin {
        animation:spin-anim 0.8s linear infinite;
        display:inline-block;
    }
    @keyframes spin-anim {
        from{transform:rotate(0deg)}
        to{transform:rotate(360deg)}
    }
`;
document.head.appendChild(extraCSS);
