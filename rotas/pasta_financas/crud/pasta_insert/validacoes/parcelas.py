def logica_parcela(valor_total, total_parcelas):
    if total_parcelas > 1:
        return list(range(1, total_parcelas + 1))
    
    return [1]