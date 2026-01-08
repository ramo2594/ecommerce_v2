"""
Costanti centralizzate per l'app shop.

In questo file mettiamo tutti i valori fissi che usiamo nel progetto.
Così se devi cambiarli, li cambi in UN SOLO POSTO.
"""

# =========================================================
# STATI DEGLI ORDINI
# =========================================================

# Costante 1: Ordine in sospeso (non ancora confermato)
ORDER_STATUS_PENDING = 'pending'

# Costante 2: Ordine confermato (pagamento ricevuto)
ORDER_STATUS_CONFIRMED = 'confirmed'

# Costante 3: Ordine spedito (in transito)
ORDER_STATUS_SHIPPED = 'shipped'

# Costante 4: Ordine consegnato (arrivato al cliente)
ORDER_STATUS_DELIVERED = 'delivered'

# Costante 5: Ordine annullato (cliente ha cancellato)
ORDER_STATUS_CANCELLED = 'cancelled'

# Lista di tuple per Django ChoiceField (mostra all'utente)
ORDER_STATUS_CHOICES = [
    (ORDER_STATUS_PENDING, 'In Sospeso'),
    (ORDER_STATUS_CONFIRMED, 'Confermato'),
    (ORDER_STATUS_SHIPPED, 'Spedito'),
    (ORDER_STATUS_DELIVERED, 'Consegnato'),
    (ORDER_STATUS_CANCELLED, 'Annullato'),
]

# ========================================================
# VALIDAZIONE PREZZI
# ========================================================

# Prezzo minimo (non puoi vendere a 0€)
MIN_PRICE = 0.01

# Prezzo massimo (limite a 999.999,99€)
MAX_PRICE = 999999,99

# ========================================================
# VALIDAZIONE QUANTITÀ
# ========================================================

# Quantità minima (non puoi ordinare 0 prodotti)
MIN_QUANTITY = 1

# Quantità massima (non puoi ordinare 1000+ prodotti)
MAX_QUANTITY = 1000

# ========================================================
# VALIDAZIONE STOCK
# ========================================================

# Stock minimo per considerare un prodotto "esaurito"
MIN_STOCK = 0

# Stock massimo (limite per il database)
MAX_STOCK = 100000