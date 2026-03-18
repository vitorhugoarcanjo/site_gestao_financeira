function formatarTelefone(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length > 10) {
        value = value.replace(/^(\d{2})(\d{5})(\d{4})/, '($1) $2-$3');
    } else if (value.length > 6) {
        value = value.replace(/^(\d{2})(\d{4})(\d{0,4})/, '($1) $2-$3');
    } else if (value.length > 2) {
        value = value.replace(/^(\d{2})(\d{0,5})/, '($1) $2');
    } else {
        value = value.replace(/^(\d{0,2})/, '($1');
    }
    
    input.value = value;
}

// Quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    const telefoneInput = document.querySelector('input[name="telefone"]');
    if (telefoneInput) {
        telefoneInput.addEventListener('input', function() {
            formatarTelefone(this);
        });
    }
});