// ==========================================================================
//  NexBankFlow Analytics -- Main Frontend Script
//  Handles: Overall Dashboard + Transaction Insight Explorer
// ==========================================================================

// Dashboard State Configuration (existing chart navigation)
const chartData = {
    'overview': {
        title: 'Transaction Amount Distribution',
        image: '/outputs/charts/01_amount_distribution.png',
        insight: 'The dataset is highly right-skewed. The average transaction (£112) is pulled up by extreme outliers despite a median of only £30.'
    },
    'demographics': {
        title: 'Customer Demographics Matrix',
        image: '/outputs/charts/10_customer_analysis.png',
        insight: 'Users aged 36-55 completely dominate the spending spectrum holding ~68.3% of total platform volume.'
    },
    'fraud': {
        title: 'Fraud Risk Distribution',
        image: '/outputs/charts/11_fraud_analysis.png',
        insight: 'Fraudulent events are significantly more frequent in international transactions (~22% rate) and peak inside the "Children" merchant category.'
    },
    'geography': {
        title: 'Global Geospatial Heatmap',
        image: '/outputs/charts/09_geographical_analysis.png',
        insight: 'The platform is intensely domestic. Over 71.2% of transactions originate firmly within the United Kingdom.'
    },
    'time': {
        title: 'Chronological Volume Analysis',
        image: '/outputs/charts/03_hourly_pattern.png',
        insight: 'Transaction volumes flatline rapidly after 21:00, with aggressive daily spikes triggering routinely at 13:00 and 16:00.'
    }
};

// ==========================================================================
//  PDF REPORT CONFIGURATION
// ==========================================================================
const pdfReportSections = [
    {
        section: 'Transaction Overview',
        charts: [
            { file: '/outputs/charts/01_amount_distribution.png', title: 'Transaction Amount Distribution', insight: 'The dataset is highly right-skewed. The average transaction (£112) is pulled up by extreme outliers despite a median of only £30.' },
            { file: '/outputs/charts/13_amount_boxplots.png', title: 'Amount Distribution Comparisons', insight: 'Box plots reveal significant variance in transaction amounts across both card types and transaction methods, with numerous high-value outliers.' }
        ]
    },
    {
        section: 'Temporal Analysis',
        charts: [
            { file: '/outputs/charts/02_day_of_week.png', title: 'Transactions by Day of Week', insight: 'Transaction volume remains relatively stable throughout the week with slight increases mid-week.' },
            { file: '/outputs/charts/03_hourly_pattern.png', title: 'Hourly Transaction Pattern', insight: 'Transaction volumes flatline rapidly after 21:00, with aggressive daily spikes triggering routinely at 13:00 and 16:00.' },
            { file: '/outputs/charts/04_time_period.png', title: 'Time Period Distribution', insight: 'Afternoon (12-17h) captures the largest transaction share, followed by a notable evening activity window.' }
        ]
    },
    {
        section: 'Card & Payment Analysis',
        charts: [
            { file: '/outputs/charts/05_card_analysis.png', title: 'Card Type & Entry Mode Analysis', insight: 'The platform processes transactions across all major card types and entry modes with balanced distribution.' },
            { file: '/outputs/charts/06_transaction_type.png', title: 'Transaction Type Analysis', insight: 'Online transactions lead in volume but POS transactions show the highest average transaction amount.' }
        ]
    },
    {
        section: 'Merchant & Bank Analysis',
        charts: [
            { file: '/outputs/charts/07_merchant_analysis.png', title: 'Merchant Group Analysis', insight: 'Merchant categories show diverse transaction patterns — Children and Electronics sectors lead in volume.' },
            { file: '/outputs/charts/08_bank_analysis.png', title: 'Bank-wise Transaction Analysis', insight: 'Transaction volumes are distributed across issuing banks with moderate concentration in top 3 institutions.' }
        ]
    },
    {
        section: 'Geography & Demographics',
        charts: [
            { file: '/outputs/charts/09_geographical_analysis.png', title: 'Geographical & International Analysis', insight: 'Over 71.2% of transactions originate within the United Kingdom. International transactions carry a higher fraud risk.' },
            { file: '/outputs/charts/10_customer_analysis.png', title: 'Customer Activity Analysis', insight: 'Users aged 36-55 completely dominate the spending spectrum holding ~68.3% of total platform volume.' }
        ]
    },
    {
        section: 'Risk & Correlation',
        charts: [
            { file: '/outputs/charts/11_fraud_analysis.png', title: 'Fraud Analysis (Descriptive)', insight: 'Fraudulent events are significantly more frequent in international transactions (~22% rate) and peak inside the "Children" merchant category.' },
            { file: '/outputs/charts/12_correlation_heatmap.png', title: 'Correlation Heatmap', insight: 'Numeric features show weak linear correlations — fraud detection likely requires non-linear models and feature interaction analysis.' }
        ]
    }
];


// ==========================================================================
//  PDF GENERATION ENGINE (preserved from original)
// ==========================================================================

function loadImage(src) {
    return new Promise((resolve, reject) => {
        const img = new Image();
        img.crossOrigin = 'anonymous';
        img.onload = () => resolve(img);
        img.onerror = () => reject(new Error(`Failed to load: ${src}`));
        img.src = src;
    });
}

function updateProgress(status, progress, percent) {
    document.getElementById('pdf-status').innerText = status;
    document.getElementById('pdf-progress').innerText = progress;
    document.getElementById('pdf-bar').style.width = percent + '%';
}

async function generatePDFReport() {
    const { jsPDF } = window.jspdf;
    const overlay = document.getElementById('pdf-overlay');
    overlay.classList.remove('hidden');

    try {
        const pdf = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'a4' });
        const pageW = 297;
        const pageH = 210;

        const brandViolet = [99, 102, 241];
        const brandIndigo = [67, 56, 202];
        const textDark = [15, 23, 42];
        const textMuted = [100, 116, 139];
        const bgLight = [241, 245, 249];

        // Cover page
        updateProgress('Building Cover Page...', 'Formatting title & metadata', 5);
        pdf.setFillColor(...brandViolet);
        pdf.rect(0, 0, pageW, 80, 'F');
        pdf.setFillColor(...brandIndigo);
        pdf.rect(0, 60, pageW, 20, 'F');
        pdf.setTextColor(255, 255, 255);
        pdf.setFontSize(36);
        pdf.setFont('helvetica', 'bold');
        pdf.text('NexBankFlow', 30, 35);
        pdf.setFontSize(16);
        pdf.setFont('helvetica', 'normal');
        pdf.text('Bank Transaction Analytics Report', 30, 48);
        pdf.setFontSize(11);
        pdf.text('Descriptive Analytics Dashboard  |  Comprehensive EDA Report', 30, 58);
        pdf.setDrawColor(255, 255, 255);
        pdf.setLineWidth(0.5);
        pdf.line(30, 64, 170, 64);

        pdf.setFontSize(12);
        pdf.setTextColor(...textDark);
        pdf.setFont('helvetica', 'bold');
        pdf.text('Report Summary', 30, 100);
        pdf.setFont('helvetica', 'normal');
        pdf.setFontSize(10);
        pdf.setTextColor(...textMuted);

        const metadata = [
            ['Dataset Period:', 'October 13 – October 16, 2020'],
            ['Total Records:', '100,000 transactions (cleaned)'],
            ['Data Integrity:', '100% — No null/duplicate rows post-cleaning'],
            ['Total Volume:', '£11,257,356'],
            ['Fraud Detection Rate:', '7.2% (7,195 flagged transactions)'],
            ['Charts Generated:', '13 analytical visualizations'],
            ['Report Generated:', new Date().toLocaleString('en-GB', { dateStyle: 'full', timeStyle: 'short' })],
        ];

        let y = 108;
        metadata.forEach(([label, value]) => {
            pdf.setFont('helvetica', 'bold');
            pdf.setTextColor(...textDark);
            pdf.text(label, 35, y);
            pdf.setFont('helvetica', 'normal');
            pdf.setTextColor(...textMuted);
            pdf.text(value, 90, y);
            y += 8;
        });

        pdf.setFontSize(12);
        pdf.setFont('helvetica', 'bold');
        pdf.setTextColor(...textDark);
        pdf.text('Sections', 30, y + 10);
        pdf.setFontSize(10);
        pdf.setFont('helvetica', 'normal');
        pdf.setTextColor(...textMuted);
        y += 18;
        pdfReportSections.forEach((section, i) => {
            pdf.text(`${i + 1}.  ${section.section}  (${section.charts.length} chart${section.charts.length > 1 ? 's' : ''})`, 35, y);
            y += 7;
        });

        pdf.setFontSize(8);
        pdf.setTextColor(180, 180, 180);
        pdf.text('Generated by NexBankFlow Analytics Dashboard', 30, pageH - 10);
        pdf.text('Confidential — Internal Use Only', pageW - 30, pageH - 10, { align: 'right' });

        // Chart pages
        let chartIndex = 0;
        const totalCharts = pdfReportSections.reduce((sum, s) => sum + s.charts.length, 0);

        for (const section of pdfReportSections) {
            for (const chart of section.charts) {
                chartIndex++;
                const pctDone = Math.round((chartIndex / totalCharts) * 90) + 5;
                updateProgress(`Rendering chart ${chartIndex}/${totalCharts}...`, `${section.section}: ${chart.title}`, pctDone);

                pdf.addPage();
                pdf.setFillColor(...bgLight);
                pdf.rect(0, 0, pageW, 28, 'F');
                pdf.setFillColor(...brandViolet);
                pdf.roundedRect(20, 8, section.section.length * 2.8 + 12, 10, 3, 3, 'F');
                pdf.setFontSize(9);
                pdf.setFont('helvetica', 'bold');
                pdf.setTextColor(255, 255, 255);
                pdf.text(section.section.toUpperCase(), 26, 14.5);

                pdf.setFontSize(16);
                pdf.setFont('helvetica', 'bold');
                pdf.setTextColor(...textDark);
                pdf.text(chart.title, 20, 42);

                try {
                    const img = await loadImage(chart.file);
                    const maxImgW = pageW - 40;
                    const maxImgH = 115;
                    const imgRatio = img.width / img.height;
                    let imgW = maxImgW;
                    let imgH = imgW / imgRatio;
                    if (imgH > maxImgH) { imgH = maxImgH; imgW = imgH * imgRatio; }
                    const imgX = (pageW - imgW) / 2;
                    const imgY = 48;
                    const canvas = document.createElement('canvas');
                    canvas.width = img.width;
                    canvas.height = img.height;
                    const ctx = canvas.getContext('2d');
                    ctx.fillStyle = '#FFFFFF';
                    ctx.fillRect(0, 0, canvas.width, canvas.height);
                    ctx.drawImage(img, 0, 0);
                    const imgData = canvas.toDataURL('image/jpeg', 0.92);
                    pdf.addImage(imgData, 'JPEG', imgX, imgY, imgW, imgH);
                } catch (e) {
                    pdf.setFontSize(12);
                    pdf.setTextColor(200, 100, 100);
                    pdf.text(`[Chart image could not be loaded: ${chart.file}]`, 20, 90);
                }

                const insightY = 170;
                pdf.setFillColor(245, 243, 255);
                pdf.roundedRect(20, insightY, pageW - 40, 24, 4, 4, 'F');
                pdf.setFillColor(...brandViolet);
                pdf.roundedRect(24, insightY + 4, 16, 16, 3, 3, 'F');
                pdf.setTextColor(255, 255, 255);
                pdf.setFontSize(12);
                pdf.text('💡', 27, insightY + 14);
                pdf.setFontSize(9);
                pdf.setFont('helvetica', 'bold');
                pdf.setTextColor(...textDark);
                pdf.text('KEY INSIGHT', 44, insightY + 8);
                pdf.setFontSize(9);
                pdf.setFont('helvetica', 'normal');
                pdf.setTextColor(...textMuted);
                const insightLines = pdf.splitTextToSize(chart.insight, pageW - 72);
                pdf.text(insightLines, 44, insightY + 14);

                pdf.setFontSize(8);
                pdf.setTextColor(180, 180, 180);
                pdf.text(`NexBankFlow Analytics Report`, 20, pageH - 6);
                pdf.text(`Page ${chartIndex + 1}`, pageW - 20, pageH - 6, { align: 'right' });
            }
        }

        updateProgress('Saving PDF...', 'Finalizing document', 98);
        await new Promise(r => setTimeout(r, 300));
        const timestamp = new Date().toISOString().slice(0, 10);
        pdf.save(`NexBankFlow_Analytics_Report_${timestamp}.pdf`);
        updateProgress('Report Exported!', 'PDF downloaded successfully ✓', 100);
        await new Promise(r => setTimeout(r, 1200));
    } catch (err) {
        console.error('PDF generation error:', err);
        updateProgress('Export Failed', err.message, 0);
        await new Promise(r => setTimeout(r, 2000));
    }

    overlay.classList.add('hidden');
}


// ==========================================================================
//  CHART.JS INSTANCES STORE (for dynamic charts)
// ==========================================================================
const chartInstances = {};

const CHART_COLORS = {
    violet: 'rgba(99, 102, 241, 0.8)',
    violetBg: 'rgba(99, 102, 241, 0.15)',
    indigo: 'rgba(67, 56, 202, 0.8)',
    orange: 'rgba(249, 115, 22, 0.8)',
    orangeBg: 'rgba(249, 115, 22, 0.15)',
    teal: 'rgba(20, 184, 166, 0.8)',
    tealBg: 'rgba(20, 184, 166, 0.15)',
    rose: 'rgba(244, 63, 94, 0.8)',
    emerald: 'rgba(16, 185, 129, 0.8)',
    emeraldBg: 'rgba(16, 185, 129, 0.15)',
    sky: 'rgba(14, 165, 233, 0.8)',
    amber: 'rgba(245, 158, 11, 0.8)',
    palette: [
        'rgba(99, 102, 241, 0.8)',
        'rgba(244, 63, 94, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(249, 115, 22, 0.8)',
        'rgba(14, 165, 233, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(168, 85, 247, 0.8)',
        'rgba(20, 184, 166, 0.8)',
        'rgba(236, 72, 153, 0.8)',
        'rgba(34, 197, 94, 0.8)',
        'rgba(59, 130, 246, 0.8)',
    ]
};

function destroyChart(id) {
    if (chartInstances[id]) {
        chartInstances[id].destroy();
        delete chartInstances[id];
    }
}

function createBarChart(canvasId, labels, data, color) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: color || CHART_COLORS.violet,
                borderRadius: 6,
                borderSkipped: false,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false }, ticks: { font: { size: 10, weight: 600 } } },
                y: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { size: 10 } } }
            }
        }
    });
}

function createLineChart(canvasId, labels, data, color) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    chartInstances[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                borderColor: color || CHART_COLORS.violet,
                backgroundColor: CHART_COLORS.violetBg,
                fill: true,
                tension: 0.4,
                pointRadius: 3,
                pointBackgroundColor: 'white',
                pointBorderColor: color || CHART_COLORS.violet,
                pointBorderWidth: 2,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { display: false }, ticks: { font: { size: 9 }, maxRotation: 45 } },
                y: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { size: 10 } } }
            }
        }
    });
}

function createDoughnutChart(canvasId, labels, data, colors) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    chartInstances[canvasId] = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || CHART_COLORS.palette.slice(0, labels.length),
                borderWidth: 2,
                borderColor: 'white',
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { font: { size: 10, weight: 600 }, padding: 10 } }
            }
        }
    });
}

function createHorizontalBarChart(canvasId, labels, data, colors) {
    destroyChart(canvasId);
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;
    chartInstances[canvasId] = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors || CHART_COLORS.palette.slice(0, labels.length),
                borderRadius: 6,
                borderSkipped: false,
            }]
        },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { grid: { color: 'rgba(0,0,0,0.04)' }, ticks: { font: { size: 10 } } },
                y: { grid: { display: false }, ticks: { font: { size: 10, weight: 600 } } }
            }
        }
    });
}


// ==========================================================================
//  EXPLORER: Filter Loading & Analysis Logic
// ==========================================================================

async function loadFilterOptions() {
    try {
        const res = await fetch('/api/filter-options');
        const data = await res.json();

        populateSelect('filter-bank', data.banks);
        populateSelect('filter-card', data.card_types);
        populateSelect('filter-entry', data.entry_modes);
        populateSelect('filter-txntype', data.txn_types);
        populateSelect('filter-merchant', data.merchant_groups);
        populateSelect('filter-country', data.countries);

        // Gender with labels
        const genderSelect = document.getElementById('filter-gender');
        data.genders.forEach(g => {
            const opt = document.createElement('option');
            opt.value = g.value;
            opt.textContent = g.label;
            genderSelect.appendChild(opt);
        });

        populateSelect('filter-age', data.age_groups);
        populateSelect('filter-fraud', data.fraud_statuses);

        // Date range
        document.getElementById('filter-date-from').min = data.date_min;
        document.getElementById('filter-date-from').max = data.date_max;
        document.getElementById('filter-date-to').min = data.date_min;
        document.getElementById('filter-date-to').max = data.date_max;

    } catch (err) {
        console.error('Failed to load filter options:', err);
    }
}

function populateSelect(id, values) {
    const select = document.getElementById(id);
    if (!select) return;
    values.forEach(v => {
        const opt = document.createElement('option');
        opt.value = v;
        opt.textContent = v;
        select.appendChild(opt);
    });
}

function getFilters() {
    return {
        bank: document.getElementById('filter-bank').value,
        card_type: document.getElementById('filter-card').value,
        entry_mode: document.getElementById('filter-entry').value,
        txn_type: document.getElementById('filter-txntype').value,
        merchant_group: document.getElementById('filter-merchant').value,
        country: document.getElementById('filter-country').value,
        gender: document.getElementById('filter-gender').value,
        age_group: document.getElementById('filter-age').value,
        fraud_status: document.getElementById('filter-fraud').value,
        date_from: document.getElementById('filter-date-from').value,
        date_to: document.getElementById('filter-date-to').value,
    };
}

function resetFilters() {
    document.getElementById('filter-bank').value = 'All';
    document.getElementById('filter-card').value = 'All';
    document.getElementById('filter-entry').value = 'All';
    document.getElementById('filter-txntype').value = 'All';
    document.getElementById('filter-merchant').value = 'All';
    document.getElementById('filter-country').value = 'All';
    document.getElementById('filter-gender').value = 'All';
    document.getElementById('filter-age').value = 'All';
    document.getElementById('filter-fraud').value = 'All';
    document.getElementById('filter-date-from').value = '';
    document.getElementById('filter-date-to').value = '';

    // Show empty state
    document.getElementById('results-empty').classList.remove('hidden');
    document.getElementById('results-content').classList.add('hidden');
    document.getElementById('results-no-data').classList.add('hidden');
    document.getElementById('results-loading').classList.add('hidden');
    document.getElementById('active-filters').innerHTML = '';
}

function showActiveFilters(filters) {
    const container = document.getElementById('active-filters');
    container.innerHTML = '';
    const labels = {
        bank: 'Bank', card_type: 'Card', entry_mode: 'Entry', txn_type: 'Txn Type',
        merchant_group: 'Merchant', country: 'Country', gender: 'Gender',
        age_group: 'Age', fraud_status: 'Fraud', date_from: 'From', date_to: 'To'
    };

    for (const [key, val] of Object.entries(filters)) {
        if (val && val !== 'All' && val !== '') {
            const displayVal = key === 'gender' ? (val === 'M' ? 'Male' : 'Female') : val;
            const tag = document.createElement('span');
            tag.className = 'active-filter-tag';
            tag.innerHTML = `<i class="fa-solid fa-filter"></i> ${labels[key]}: ${displayVal}`;
            container.appendChild(tag);
        }
    }
}

async function runAnalysis() {
    const filters = getFilters();
    const analyzeBtn = document.getElementById('analyze-btn');

    // Show loading
    analyzeBtn.classList.add('loading');
    analyzeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> ANALYZING...';
    document.getElementById('results-empty').classList.add('hidden');
    document.getElementById('results-content').classList.add('hidden');
    document.getElementById('results-no-data').classList.add('hidden');
    document.getElementById('results-loading').classList.remove('hidden');

    showActiveFilters(filters);

    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(filters)
        });
        const data = await res.json();

        document.getElementById('results-loading').classList.add('hidden');

        if (data.num_results === 0 || !data.statistics) {
            document.getElementById('results-no-data').classList.remove('hidden');
        } else {
            displayResults(data);
            document.getElementById('results-content').classList.remove('hidden');
        }
    } catch (err) {
        console.error('Analysis failed:', err);
        document.getElementById('results-loading').classList.add('hidden');
        document.getElementById('results-no-data').classList.remove('hidden');
    }

    analyzeBtn.classList.remove('loading');
    analyzeBtn.innerHTML = '<i class="fa-solid fa-bolt"></i> ANALYZE';
}


// ==========================================================================
//  DISPLAY RESULTS
// ==========================================================================

function fmtNum(n) {
    if (n === null || n === undefined) return '—';
    return n.toLocaleString('en-GB', { maximumFractionDigits: 2 });
}

function fmtCurrency(n) {
    if (n === null || n === undefined) return '—';
    return '£' + n.toLocaleString('en-GB', { maximumFractionDigits: 2 });
}

function displayResults(data) {
    const stats = data.statistics;

    // Summary badge
    document.getElementById('result-count').textContent = fmtNum(stats.num_transactions);
    const pctBadge = document.getElementById('result-pct');
    if (stats.segment_pct_of_total) {
        pctBadge.textContent = `${stats.segment_pct_of_total}% of total dataset`;
    } else {
        pctBadge.textContent = '';
    }

    // KPI Grid
    const kpiGrid = document.getElementById('kpi-grid');
    kpiGrid.innerHTML = '';

    const kpis = [
        { label: 'Transactions', value: fmtNum(stats.num_transactions), color: 'violet', sub: '' },
        { label: 'Total Amount', value: fmtCurrency(stats.total_amount), color: 'indigo', sub: '' },
        { label: 'Average Amount', value: fmtCurrency(stats.avg_amount), color: 'teal', sub: stats.overall_avg_amount ? `Overall: ${fmtCurrency(stats.overall_avg_amount)}` : '' },
        { label: 'Median Amount', value: fmtCurrency(stats.median_amount), color: 'emerald', sub: '' },
        { label: 'Min Amount', value: fmtCurrency(stats.min_amount), color: 'sky', sub: '' },
        { label: 'Max Amount', value: fmtCurrency(stats.max_amount), color: 'amber', sub: '' },
        { label: 'Most Active Day', value: stats.most_active_day || '—', color: 'violet', sub: stats.most_active_day_count ? `${fmtNum(stats.most_active_day_count)} txns` : '' },
        { label: 'Peak Hour', value: stats.peak_hour !== undefined ? `${stats.peak_hour}:00` : '—', color: 'orange', sub: stats.peak_hour_count ? `${fmtNum(stats.peak_hour_count)} txns` : '' },
        { label: 'Peak Time Period', value: stats.peak_time_period || '—', color: 'rose', sub: stats.peak_time_period_pct ? `${stats.peak_time_period_pct}%` : '' },
        { label: 'Most Used Card', value: stats.most_used_card || '—', color: 'indigo', sub: stats.most_used_card_pct ? `${stats.most_used_card_pct}%` : '' },
        { label: 'Common Entry Mode', value: stats.most_common_entry_mode || '—', color: 'teal', sub: stats.most_common_entry_mode_pct ? `${stats.most_common_entry_mode_pct}%` : '' },
        { label: 'Top Merchant', value: stats.top_merchant || '—', color: 'emerald', sub: stats.top_merchant_pct ? `${stats.top_merchant_pct}%` : '' },
        { label: 'Common Txn Type', value: stats.most_common_txn_type || '—', color: 'sky', sub: stats.most_common_txn_type_pct ? `${stats.most_common_txn_type_pct}%` : '' },
        { label: 'Top Country', value: stats.top_country || '—', color: 'amber', sub: stats.top_country_pct ? `${stats.top_country_pct}%` : '' },
        { label: 'Fraud Rate', value: stats.fraud_pct !== undefined ? `${stats.fraud_pct}%` : '—', color: 'rose', sub: stats.fraud_count ? `${fmtNum(stats.fraud_count)} flagged` : '' },
    ];

    kpis.forEach(kpi => {
        const card = document.createElement('div');
        card.className = `kpi-mini-card ${kpi.color}`;
        card.innerHTML = `
            <span class="kpi-label">${kpi.label}</span>
            <span class="kpi-value">${kpi.value}</span>
            ${kpi.sub ? `<span class="kpi-sub">${kpi.sub}</span>` : ''}
        `;
        kpiGrid.appendChild(card);
    });

    // Deeper Stats Grid
    const deepGrid = document.getElementById('deep-stats-grid');
    deepGrid.innerHTML = '';

    const deepStats = [
        { label: 'Std Deviation', value: fmtCurrency(stats.std_amount) },
        { label: 'Variance', value: fmtCurrency(stats.variance_amount) },
        { label: 'Q1 (25th)', value: fmtCurrency(stats.q1_amount) },
        { label: 'Q3 (75th)', value: fmtCurrency(stats.q3_amount) },
        { label: 'IQR', value: fmtCurrency(stats.iqr_amount) },
        { label: 'P10', value: fmtCurrency(stats.p10_amount) },
        { label: 'P90', value: fmtCurrency(stats.p90_amount) },
        { label: 'Mode', value: stats.mode_amount !== null ? fmtCurrency(stats.mode_amount) : '—' },
        { label: 'Outliers', value: `${fmtNum(stats.outlier_count)} (${stats.outlier_pct}%)` },
        { label: 'Avg Age', value: stats.avg_age ? `${stats.avg_age} yrs` : '—' },
        { label: 'Median Age', value: stats.median_age ? `${stats.median_age} yrs` : '—' },
        { label: 'Amount Ratio', value: stats.avg_amount_vs_overall ? `${stats.avg_amount_vs_overall}x` : '—' },
    ];

    deepStats.forEach(ds => {
        const item = document.createElement('div');
        item.className = 'deep-stat-item';
        item.innerHTML = `<div class="ds-label">${ds.label}</div><div class="ds-value">${ds.value}</div>`;
        deepGrid.appendChild(item);
    });

    // Charts
    if (data.chart_data) {
        renderDynamicCharts(data.chart_data);
    }

    // Insights
    const insightsList = document.getElementById('insights-list');
    insightsList.innerHTML = '';
    if (data.insights && data.insights.length > 0) {
        data.insights.forEach((insight, idx) => {
            const item = document.createElement('div');
            item.className = 'insight-item';
            item.innerHTML = `
                <div class="insight-bullet">${idx + 1}</div>
                <div class="insight-text">${insight}</div>
            `;
            insightsList.appendChild(item);
        });
    }

    // Suggestions
    const suggestionsList = document.getElementById('suggestions-list');
    suggestionsList.innerHTML = '';
    if (data.suggestions && data.suggestions.length > 0) {
        data.suggestions.forEach(suggestion => {
            const item = document.createElement('div');
            item.className = 'suggestion-item';
            item.innerHTML = `
                <div class="suggestion-icon"><i class="fa-solid fa-arrow-right"></i></div>
                <div class="suggestion-text">${suggestion}</div>
            `;
            suggestionsList.appendChild(item);
        });
    }
}

function renderDynamicCharts(chartData) {
    // Day of Week
    if (chartData.day_of_week) {
        createBarChart('chart-day', chartData.day_of_week.labels, chartData.day_of_week.values, CHART_COLORS.violet);
    }

    // Hourly
    if (chartData.hourly) {
        createLineChart('chart-hourly', chartData.hourly.labels, chartData.hourly.values, CHART_COLORS.rose);
    }

    // Time period
    if (chartData.time_period) {
        createDoughnutChart('chart-period', chartData.time_period.labels, chartData.time_period.values);
    }

    // Card type
    if (chartData.card_type) {
        createDoughnutChart('chart-card', chartData.card_type.labels, chartData.card_type.values,
            [CHART_COLORS.violet, CHART_COLORS.rose]);
    }

    // Merchant
    if (chartData.merchant) {
        createHorizontalBarChart('chart-merchant', chartData.merchant.labels, chartData.merchant.values);
    }

    // Transaction type
    if (chartData.txn_type) {
        createBarChart('chart-txntype', chartData.txn_type.labels, chartData.txn_type.values, CHART_COLORS.teal);
    }

    // Amount distribution
    if (chartData.amount_distribution) {
        createBarChart('chart-amount', chartData.amount_distribution.labels, chartData.amount_distribution.values, CHART_COLORS.emerald);
    }

    // Trend
    if (chartData.trend) {
        createLineChart('chart-trend', chartData.trend.labels, chartData.trend.values, CHART_COLORS.violet);
    }
}


// ==========================================================================
//  SECTION NAVIGATION (Overall vs Explorer)
// ==========================================================================

function switchSection(target) {
    const overallSection = document.getElementById('section-overall');
    const explorerSection = document.getElementById('section-explorer');

    if (target === 'explorer') {
        overallSection.classList.add('hidden');
        explorerSection.classList.remove('hidden');
    } else {
        overallSection.classList.remove('hidden');
        explorerSection.classList.add('hidden');
    }
}


// ==========================================================================
//  MAIN DOM READY
// ==========================================================================
document.addEventListener('DOMContentLoaded', () => {
    
    // 1. Cursor Follower Logic
    const cursor = document.getElementById('cursor-follower');
    document.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    });

    const clickables = document.querySelectorAll('button, .tilt-card, .kpi-mini-card, select');
    clickables.forEach(el => {
        el.addEventListener('mouseenter', () => cursor.classList.add('active'));
        el.addEventListener('mouseleave', () => cursor.classList.remove('active'));
    });

    // 2. Animate KPI Counters
    const counters = document.querySelectorAll('.counter');
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.getAttribute('data-target');
            const count = +counter.innerText.replace(/,/g, '');
            const inc = target / 50;

            if (count < target) {
                let newCount = count + inc;
                if (target % 1 !== 0) newCount = newCount.toFixed(2);
                else newCount = Math.ceil(newCount);
                
                counter.innerText = newCount.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
                setTimeout(updateCount, 40);
            } else {
                counter.innerText = target.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
            }
        };
        setTimeout(updateCount, 800);
    });

    // 3. 3D Tilt Effect on KPI Cards
    const tiltCards = document.querySelectorAll('.tilt-card');
    tiltCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            const rotateX = ((y - centerY) / centerY) * -10;
            const rotateY = ((x - centerX) / centerX) * 10;
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.02, 1.02, 1.02)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = `perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)`;
            card.style.transition = 'transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
        });
        card.addEventListener('mouseenter', () => {
            card.style.transition = 'transform 0.1s';
        });
    });

    // 4. Interactive Chart Navigation + Section Switching
    const navPills = document.querySelectorAll('.nav-pill');
    const mainChartImg = document.getElementById('main-chart-img');
    const chartTitle = document.getElementById('dynamic-title');
    const insightText = document.getElementById('dynamic-insight');
    const loader = document.getElementById('loader');

    navPills.forEach(pill => {
        pill.addEventListener('click', () => {
            if (pill.classList.contains('active')) return;

            navPills.forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            const target = pill.getAttribute('data-target');

            // Switch between Explorer and Overall views
            if (target === 'explorer') {
                switchSection('explorer');
                return;
            } else {
                switchSection('overall');
            }

            const data = chartData[target];
            if (data) {
                loader.classList.remove('hidden');
                mainChartImg.style.opacity = 0;

                setTimeout(() => {
                    chartTitle.innerText = data.title;
                    insightText.innerText = data.insight;
                    mainChartImg.src = data.image;
                    
                    mainChartImg.onload = () => {
                        loader.classList.add('hidden');
                        mainChartImg.style.opacity = 1;
                    };
                }, 300);
            }
        });
    });

    // 5. PDF Export Button
    const exportBtn = document.getElementById('export-pdf-btn');
    if (exportBtn) {
        exportBtn.addEventListener('click', () => {
            generatePDFReport();
        });
    }

    // 6. Theme Toggle Logic
    const themeBtn = document.getElementById('theme-toggle-btn');
    const savedTheme = localStorage.getItem('nexbank-theme');
    if (savedTheme === 'dark') {
        document.documentElement.classList.add('dark-mode');
        document.body.classList.add('dark-mode');
    }

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = document.body.classList.toggle('dark-mode');
            document.documentElement.classList.toggle('dark-mode', isDark);
            localStorage.setItem('nexbank-theme', isDark ? 'dark' : 'light');
        });
    }

    // 7. Chart Lightbox / Zoom Logic
    const zoomBtn = document.getElementById('zoom-chart-btn');
    const lightbox = document.getElementById('chart-lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxTitle = document.getElementById('lightbox-title');
    const lightboxClose = document.getElementById('lightbox-close');

    if (zoomBtn && lightbox && lightboxImg) {
        zoomBtn.addEventListener('click', () => {
            const currentImg = document.getElementById('main-chart-img');
            const currentTitle = document.getElementById('dynamic-title');
            if (currentImg && currentTitle) {
                lightboxImg.src = currentImg.src;
                lightboxTitle.textContent = currentTitle.textContent;
                lightbox.classList.remove('hidden');
            }
        });

        if (lightboxClose) {
            lightboxClose.addEventListener('click', () => {
                lightbox.classList.add('hidden');
            });
        }

        lightbox.addEventListener('click', (e) => {
            if (e.target === lightbox) {
                lightbox.classList.add('hidden');
            }
        });
    }

    // 8. Explorer: Load filter options & attach event listeners
    loadFilterOptions();

    const analyzeBtn = document.getElementById('analyze-btn');
    if (analyzeBtn) {
        analyzeBtn.addEventListener('click', () => {
            runAnalysis();
        });
    }

    const resetBtn = document.getElementById('reset-filters-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            resetFilters();
        });
    }
});
