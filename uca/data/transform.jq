select(.id != "")
| select(.value > 0)
| del(.metadata, .uca)