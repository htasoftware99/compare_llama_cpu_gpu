# import time
# import requests
# import psutil
# from tabulate import tabulate
# import json
# from py3nvml import py3nvml  # GPU kullanımını daha doğru izlemek için

# # Yeni model isimleri ve portlar
# MODELS = [
#     "llama3.2:1b-instruct-q4_K_M",
#     "llama3.2:1b-instruct-q5_K_S",
#     "llama3.2:1b-instruct-q6_K",
#     "llama3.2:3b-instruct-q4_K_M",
#     "llama3.2:3b-instruct-q5_K_S",
#     "llama3.2:3b-instruct-q6_K"
# ]
# PORTS = [11460, 11461, 11462, 11463, 11464, 11465]

# # MODELS sözlüğünü model ismi: API URL olacak şekilde oluşturuyoruz.
# model_urls = {model: f"http://127.0.0.1:{port}/api/generate" for model, port in zip(MODELS, PORTS)}

# PROMPT = "what is glioma?"

# # GPU kullanımını daha doğru almak için py3nvml kullanıyoruz
# py3nvml.nvmlInit()

# def get_gpu_usage():
#     """NVIDIA GPU kullanımını döndürür (yüzde cinsinden)."""
#     try:
#         handle = py3nvml.nvmlDeviceGetHandleByIndex(0)  # GPU0'ı kullanıyoruz
#         gpu_util = py3nvml.nvmlDeviceGetUtilizationRates(handle)
#         return gpu_util.gpu  # GPU kullanım oranını döndürür
#     except Exception as e:
#         print(f"GPU kullanımı alınırken hata: {e}")
#         return "N/A"

# def parse_streaming_response(response):
#     """Streaming yanıtı satır satır işleyip tam yanıtı oluşturur."""
#     complete_response = ""
#     for line in response.iter_lines():
#         if line:
#             try:
#                 # Her satırı ayrı ayrı JSON'a çeviriyoruz
#                 data = json.loads(line.decode('utf-8'))
#                 complete_response += data.get("response", "")
#             except Exception as e:
#                 print(f"Satır parse hatası: {e}")
#     return complete_response

# def test_model(model_name, api_url):
#     """Belirtilen modele istek atarak yanıt süresini, sistem kullanımını ve modelin yanıtını ölçer."""
#     # CPU ölçümüne başlamadan önce kısa bir gecikme ekliyoruz
#     time.sleep(0.1)
    
#     cpu_before = psutil.cpu_percent(interval=1)
#     mem_before = psutil.virtual_memory().percent
#     gpu_before = get_gpu_usage()
    
#     start_time = time.time()
    
#     # Hata ayıklama için debug bilgisi
#     print(f"\nDebug - İstek atılıyor: {api_url}")
    
#     try:
#         # Streaming yanıtı işlemek için stream=True ekleniyor
#         response = requests.post(api_url, json={"prompt": PROMPT, "model": model_name}, timeout=10, stream=True)
#         response_time = time.time() - start_time
        
#         print(f"Debug - Yanıt alındı - Status code: {response.status_code}")
        
#         if response.status_code == 200:
#             # Streaming yanıtı satır satır işleyip birleştiriyoruz
#             model_response = parse_streaming_response(response)
#             print(f"Debug - Tam yanıt: {model_response}")
#         else:
#             model_response = f"Hata kodu: {response.status_code}, Yanıt: {response.text[:100]}"
    
#     except Exception as e:
#         print(f"Debug - İstek hatası: {str(e)}")
#         model_response = f"İstek hatası: {str(e)}"
#         response_time = time.time() - start_time
    
#     # CPU, RAM ve GPU kullanımlarını tekrar ölçüyoruz
#     cpu_after = psutil.cpu_percent(interval=1)
#     mem_after = psutil.virtual_memory().percent
#     gpu_after = get_gpu_usage()
    
#     latency = round(response_time * 1000, 2)  # ms cinsinden
#     cpu_usage = round(cpu_after - cpu_before, 2)
#     mem_usage = round(mem_after - mem_before, 2)
    
#     return [model_name, latency, cpu_usage, mem_usage, gpu_after, model_response]

# def main():
#     results = []
#     response_details = []
#     print("Benchmarking started...\n")
    
#     # model_urls sözlüğü üzerinden iterasyon
#     for model, url in model_urls.items():
#         print(f"\n--- Test ediliyor: {model} ---")
#         try:
#             result = test_model(model, url)
#             results.append(result[:5])  # Performans metriklerini ayrı sakla
#             response_details.append([model, result[5]])  # Model ve yanıtı ayrı sakla
#         except Exception as e:
#             error_msg = f"Hata: {str(e)}"
#             print(error_msg)
#             results.append([model, "Error", "Error", "Error", "Error"])
#             response_details.append([model, error_msg])
    
#     # Performans sonuçlarını tablo olarak göster
#     print("\n=== PERFORMANS METRİKLERİ ===")
#     print(tabulate(results, headers=["Model", "Latency (ms)", "CPU (%)", "RAM (%)", "GPU (%)"], tablefmt="grid"))
    
#     # Model yanıtlarını göster
#     print("\n=== MODEL YANITLARI ===")
#     for model_data in response_details:
#         print(f"\n{model_data[0]}:")
#         print("-" * len(model_data[0]))
#         print(f"Soru: {PROMPT}")
#         print(f"Yanıt: {model_data[1]}")

# if __name__ == "__main__":
#     main()


import time
import requests
import psutil
from tabulate import tabulate
import json
from py3nvml import py3nvml  # GPU kullanımını daha doğru izlemek için

# Yeni model isimleri ve portlar
MODELS = [
    "llama3.2:1b-instruct-q4_K_M",
    "llama3.2:1b-instruct-q5_K_S",
    "llama3.2:1b-instruct-q6_K",
    "llama3.2:3b-instruct-q4_K_M",
    "llama3.2:3b-instruct-q5_K_S",
    "llama3.2:3b-instruct-q6_K"
]
PORTS = [11460, 11461, 11462, 11463, 11464, 11465]

# MODELS sözlüğünü model ismi: API URL olacak şekilde oluşturuyoruz.
model_urls = {model: f"http://127.0.0.1:{port}/api/generate" for model, port in zip(MODELS, PORTS)}

PROMPT = "what is glioma?"

# GPU kullanımını daha doğru almak için py3nvml kullanıyoruz
py3nvml.nvmlInit()

def get_gpu_memory_usage():
    """NVIDIA GPU hafıza kullanımını döndürür (MB cinsinden)."""
    try:
        handle = py3nvml.nvmlDeviceGetHandleByIndex(0)  # GPU0'ı kullanıyoruz
        memory_info = py3nvml.nvmlDeviceGetMemoryInfo(handle)
        return memory_info.used / (1024 * 1024)  # Kullanılan hafızayı MB cinsinden döndürür
    except Exception as e:
        print(f"GPU hafıza kullanımı alınırken hata: {e}")
        return "N/A"

def parse_streaming_response(response):
    """Streaming yanıtı satır satır işleyip tam yanıtı oluşturur."""
    complete_response = ""
    for line in response.iter_lines():
        if line:
            try:
                # Her satırı ayrı ayrı JSON'a çeviriyoruz
                data = json.loads(line.decode('utf-8'))
                complete_response += data.get("response", "")
            except Exception as e:
                print(f"Satır parse hatası: {e}")
    return complete_response

def test_model(model_name, api_url):
    """Belirtilen modele istek atarak yanıt süresini, sistem kullanımını ve modelin yanıtını ölçer."""
    # CPU ölçümüne başlamadan önce kısa bir gecikme ekliyoruz
    time.sleep(0.1)
    
    cpu_before = psutil.cpu_percent(interval=1)
    mem_before = psutil.virtual_memory().percent
    gpu_before = get_gpu_memory_usage()  # GPU hafıza kullanımı MB
    
    start_time = time.time()
    
    # Hata ayıklama için debug bilgisi
    print(f"\nDebug - İstek atılıyor: {api_url}")
    
    try:
        # Streaming yanıtı işlemek için stream=True ekleniyor
        response = requests.post(api_url, json={"prompt": PROMPT, "model": model_name}, timeout=10, stream=True)
        response_time = time.time() - start_time
        
        print(f"Debug - Yanıt alındı - Status code: {response.status_code}")
        
        if response.status_code == 200:
            # Streaming yanıtı satır satır işleyip birleştiriyoruz
            model_response = parse_streaming_response(response)
            print(f"Debug - Tam yanıt: {model_response}")
        else:
            model_response = f"Hata kodu: {response.status_code}, Yanıt: {response.text[:100]}"
    
    except Exception as e:
        print(f"Debug - İstek hatası: {str(e)}")
        model_response = f"İstek hatası: {str(e)}"
        response_time = time.time() - start_time
    
    # CPU, RAM ve GPU kullanımlarını tekrar ölçüyoruz
    cpu_after = psutil.cpu_percent(interval=1)
    mem_after = psutil.virtual_memory().percent
    gpu_after = get_gpu_memory_usage()  # GPU hafıza kullanımı MB
    
    latency = round(response_time * 1000, 2)  # ms cinsinden
    cpu_usage = round(cpu_after - cpu_before, 2)
    mem_usage = round(mem_after - mem_before, 2)
    
    return [model_name, latency, cpu_usage, mem_usage, gpu_after, model_response]

def main():
    results = []
    response_details = []
    print("Benchmarking started...\n")
    
    # model_urls sözlüğü üzerinden iterasyon
    for model, url in model_urls.items():
        print(f"\n--- Test ediliyor: {model} ---")
        try:
            result = test_model(model, url)
            results.append(result[:5])  # Performans metriklerini ayrı sakla
            response_details.append([model, result[5]])  # Model ve yanıtı ayrı sakla
        except Exception as e:
            error_msg = f"Hata: {str(e)}"
            print(error_msg)
            results.append([model, "Error", "Error", "Error", "Error"])
            response_details.append([model, error_msg])
    
    # Performans sonuçlarını tablo olarak göster
    print("\n=== PERFORMANS METRİKLERİ ===")
    print(tabulate(results, headers=["Model", "Latency (ms)", "CPU (%)", "RAM (%)", "GPU Memory (MB)"], tablefmt="grid"))
    
    # Model yanıtlarını göster
    print("\n=== MODEL YANITLARI ===")
    for model_data in response_details:
        print(f"\n{model_data[0]}:")
        print("-" * len(model_data[0]))
        print(f"Soru: {PROMPT}")
        print(f"Yanıt: {model_data[1]}")

if __name__ == "__main__":
    main()
