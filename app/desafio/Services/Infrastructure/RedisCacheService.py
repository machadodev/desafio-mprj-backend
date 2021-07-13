from django.core.cache import cache
from desafio.Services.Protocols import CacheService


class RedisCacheService(CacheService):
    def __init__(self, TTL_IN_SECONDS):
        self.TTL_IN_SECONDS = TTL_IN_SECONDS
        
    def get(self, key):
        print("BUSCANDO CHAVE NO CACHE:", key)
        #return cache.get(key, None)
        return None
    
    def set(self, key, value):
        print("CACHE CRIADO - CHAVE:", key, "VALOR:", value)
        pass
    def delete(self, key):
        print("CACHE DELETADO:", key)
        pass