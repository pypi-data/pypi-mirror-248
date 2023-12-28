import lemon_rag
lemon_rag.patch_all(lemon)
print(lemon_rag.lemon_models.models.AuthUserTab.select())