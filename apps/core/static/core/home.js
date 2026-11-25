document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#window-calculator');
    const preview = document.querySelector('#window-preview');
    const materialSelect = form.elements.material;
    const materialImage = document.querySelector('#material-preview-image');
    const previewLabel = document.querySelector('#calculator-preview-label');
    const error = document.querySelector('#calculator-error');
    const result = document.querySelector('#calculator-result');
    const priceOutput = document.querySelector('#calculator-price');
    const detailsOutput = document.querySelector('#calculator-details');
    const orderLink = document.querySelector('#calculator-order');
    const widthInput = form.elements.width;
    const heightInput = form.elements.height;
    const quantityInput = form.elements.quantity;
    let lastTouchTap = 0;
    let lastTouchZoom = 0;

    const updateMaterialPreview = () => {
        const selectedOption = materialSelect.selectedOptions[0];
        const materialName = selectedOption?.dataset.materialName;
        const materialSlug = selectedOption?.dataset.materialSlug?.toLowerCase() || '';
        const imagePath = selectedOption?.dataset.image;

        if (!materialName) {
            return;
        }

        preview.classList.remove(
            'window-preview--material-pvc',
            'window-preview--material-aluminum',
            'window-preview--material-wood',
        );
        if (/(?:alumin|alyum)/.test(materialSlug) || materialName.toLocaleLowerCase('ru').includes('алюмин')) {
            preview.classList.add('window-preview--material-aluminum');
        } else if (/(?:wood|derev)/.test(materialSlug) || materialName.toLocaleLowerCase('ru').includes('дерев')) {
            preview.classList.add('window-preview--material-wood');
        } else if (/(?:pvc|pvk|plast)/.test(materialSlug) || /пвх|пластик/i.test(materialName)) {
            preview.classList.add('window-preview--material-pvc');
        }

        previewLabel.textContent = `Материал: ${materialName}`;
        if (!imagePath) {
            materialImage.hidden = true;
            preview.classList.remove('window-preview--has-image');
            preview.setAttribute(
                'aria-label',
                `Окно с рамой из материала «${materialName}». Дважды нажмите, чтобы увеличить изображение.`,
            );
            return;
        }

        const imageUrl = new URL(imagePath, document.baseURI).href;
        materialImage.alt = `Изображение материала «${materialName}»`;
        materialImage.onerror = () => {
            if (materialImage.src === imageUrl) {
                materialImage.hidden = true;
                preview.classList.remove('window-preview--has-image');
            }
        };
        materialImage.src = imageUrl;
        materialImage.hidden = false;
        preview.classList.add('window-preview--has-image');
        preview.setAttribute(
            'aria-label',
            `Материал: ${materialName}. Дважды нажмите, чтобы увеличить изображение.`,
        );
    };

    const toggleZoom = () => {
        const zoomed = preview.classList.toggle('window-preview--zoomed');
        preview.setAttribute('aria-pressed', String(zoomed));
    };

    preview.addEventListener('dblclick', () => {
        if (Date.now() - lastTouchZoom > 500) {
            toggleZoom();
        }
    });

    preview.addEventListener('pointerup', (event) => {
        if (event.pointerType !== 'touch') {
            return;
        }
        const now = Date.now();
        if (now - lastTouchTap < 350) {
            toggleZoom();
            lastTouchZoom = now;
            lastTouchTap = 0;
        } else {
            lastTouchTap = now;
        }
    });

    const updatePreview = () => {
        const width = Number(widthInput.value);
        const height = Number(heightInput.value);
        if (width > 0 && height > 0) {
            const ratio = Math.min(1.7, Math.max(0.55, width / height));
            preview.style.setProperty('--window-ratio', ratio.toFixed(2));
        }
    };

    const invalidateQuote = () => {
        result.hidden = true;
        error.hidden = true;
    };

    widthInput.addEventListener('input', updatePreview);
    heightInput.addEventListener('input', updatePreview);
    [widthInput, heightInput, quantityInput].forEach((input) => {
        input.addEventListener('input', invalidateQuote);
    });
    materialSelect.addEventListener('change', () => {
        updateMaterialPreview();
        invalidateQuote();
    });
    updatePreview();
    updateMaterialPreview();

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        error.hidden = true;
        result.hidden = true;

        try {
            const response = await fetch(form.action, {
                method: 'POST',
                body: new FormData(form),
                headers: {
                    'X-CSRFToken': form.elements.csrfmiddlewaretoken.value,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin',
            });
            const quote = await response.json();
            if (!response.ok) {
                throw new Error(quote.error || 'Не удалось рассчитать стоимость. Попробуйте ещё раз.');
            }

            const formatter = new Intl.NumberFormat('ru-RU', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2,
            });
            priceOutput.textContent = `${formatter.format(Number(quote.total_price))} ${quote.currency}`;
            detailsOutput.textContent = `${quote.material} · ${quote.area} м² · ${quote.quantity} шт.`;
            const orderDetails = new URLSearchParams();
            ['material', 'width', 'height', 'quantity'].forEach((field) => {
                orderDetails.set(field, form.elements[field].value);
            });
            const profileUrl = new URL(form.dataset.profileUrl, window.location.origin);
            profileUrl.search = orderDetails.toString();
            profileUrl.hash = 'orders';
            if (form.dataset.authenticated === 'true') {
                orderLink.href = profileUrl.href;
            } else {
                const loginUrl = new URL(form.dataset.loginUrl, window.location.origin);
                loginUrl.searchParams.set(
                    'next',
                    `${profileUrl.pathname}${profileUrl.search}${profileUrl.hash}`,
                );
                orderLink.href = loginUrl.href;
            }
            result.hidden = false;
        } catch (requestError) {
            error.textContent = requestError instanceof Error
                ? requestError.message
                : 'Не удалось рассчитать стоимость. Проверьте соединение и попробуйте ещё раз.';
            error.hidden = false;
        }
    });
});
