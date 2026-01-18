document.addEventListener('DOMContentLoaded', function() {
    const orderBtn = document.getElementById('order-btn');
    
    if (orderBtn) {
        // Auto-trigger dopo 2 secondi
        setTimeout(() => {
            orderBtn.click();
        }, 2000);
        
        orderBtn.addEventListener('click', function() {
            if (this.classList.contains('animating')) return;
            
            this.classList.add('animating', 'animatetruck');
            const success = this.querySelector('.success');
            success.classList.add('active');
            
            // Checkmark animazione
            const polyline = success.querySelector('polyline');
            polyline.style.strokeDashoffset = '20';
            polyline.style.animation = 'checkmark 0.5s ease 0.5s forwards';
        });
    }
});
