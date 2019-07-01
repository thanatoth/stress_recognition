import urllib.request, urllib.parse, json, base64

#jsonデータを返却する
# {'name': value, 'name2': value2, 'name3': value3} の形で帰ってくる

def getSoracom():
    #データをリクエスト
    headers = {"Accept":"application/json",
    "X-Soracom-API-Key":"api-fda2a6a1-bcf8-46a6-9937-fdadee4ab5c8",
    "X-Soracom-Token":"eyJraWQiOiJBUUVDQUhnYmdGdnFrclRTbGlNVmNCQnV0VXlVcnNvU1RqTTM4NlR5WGVsaEdlUWtOd0FBQVk0d2dnR0tCZ2txaGtpRzl3MEJCd2FnZ2dGN01JSUJkd0lCQURDQ0FYQUdDU3FHU0liM0RRRUhBVEFlQmdsZ2hrZ0JaUU1FQVM0d0VRUU1BYk5RSkQ0aW1QWE9NbjIrQWdFUWdJSUJRZGxDb2VoTmxLTFE4Y3FyRlRGUURmYkszRXV0NGlWTlJydU05LzR1N2ZLZVZmQTVKZkpyRzZ6Ymx0WnRPdXhsV3ZhRWpZTVY5U2NhdmRrRnA5cVBqbzMrb0ZFQ2RFTFZ6N2F4ZUZnQW4xQlpwU1kzOUNMWFE3SHR4QzhvTjN6cDJzVVdiUUYyZ3Z0cTNVUFVETEcrWkg1N0N1NVBKYUs0QlBHTW5TRlZXSjVIeFh4OEs0K2F6czdiNFlVbGtWcVZQQnVGaTBQanI4NXR0VnF0ZGZPQUhtL2t3TzlDcDAxamowejcvZjBpUDVvRDZtdkJ2eUJCdEVxR2VmS2pReHdMWnFSWU1YVWttMWJsa21VdXovbkVJQU1aREUzRHRMOWpjMVJuVGlRRm1oVi9IaTUxMGxobmczTXpONTR2bWpZUHE0dDJZakNzcjhlTWRqbHVWWjA1VFRWSzFQcklKR3RVaERRNzA4eHo1YUw2SjFyWUxBUXBTdm45QmM1WUtBWmY3emJ2bUFlK0EyVG9GSWJ5SGcvaUdCbEFYTFAwTUhwME9XejBuSlpPUTBQaEt3PT0iLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJzb3JhY29tLmlvIiwiYXVkIjoiT3BlcmF0b3IiLCJleHAiOjE1NjE5MzgyNzIsImp0aSI6Ik5wcmJNRWE0VFhsaHJMaXFBZUFwTVEiLCJpYXQiOjE1NjE4NTE4NzIsIm5iZiI6MTU2MTg1MTc1Miwic3ViIjoic29yYWNvbSIsIm9wZXJhdG9yIjp7ImNvdmVyYWdlVHlwZXMiOlsianAiLCJnIl0sInBlcm1pc3Npb25zIjpbeyJzdGF0ZW1lbnRzIjpbeyJlZmZlY3QiOiJhbGxvdyIsImFwaSI6WyIqIl19XX1dLCJhY2NvdW50VHlwZSI6IjAiLCJ1c2VyTmFtZSI6ImtkZzIwMTkwMSIsInBheW1lbnRNZXRob2RTdGF0dXMiOiJyZWdpc3RlcmVkIiwib3BlcmF0b3JJZCI6Ik9QMDA5MDEyNTc2OSIsImNvdmVyYWdlVHlwZUF0dHJpYnV0ZXMiOnsianAiOnsidGVybXNWZXJzaW9uIjoiMSIsInBheW1lbnRNZXRob2RTdGF0dXMiOiJyZWdpc3RlcmVkIiwiY29udHJhY3RzIjpbXSwiY29udHJhY3REZXRhaWwiOnt9fSwiZyI6eyJ0ZXJtc1ZlcnNpb24iOiIxIiwicGF5bWVudE1ldGhvZFN0YXR1cyI6InVucmVnaXN0ZXJlZCIsImNvbnRyYWN0cyI6W10sImNvbnRyYWN0RGV0YWlsIjp7fX19fX0.xEe4C47CRq8I3-0D_fAkqIcS0oskvM7Ue4JEfX7VnDh7mdtA3TvXXFUZCZMlgbFA0nDdA59GBYQuYFFy1Sq1rz_TXDPDjooJ5RPPR23wzIcjbDSY9WzikLzii2ez3MeONrnvODNCGaZ162LTa6L_sLg7801-IYlyJ69GAyutrPyI9bM-28xFxCCwsQZ1AXpRz9ipjhits8_wGs6vdn8hDlDGjjjzeZGYzoyRpD5Jo2vbCW7nrU1SEcRKpWLP4_PNxczAt9IFntDKdjrYGZNQWTQn0Okw_QW72swVoBwJcrOTVhqydUlIw7UOzMB5XSHldXdEk8wCQRfgrYnORobpmg"}

    req = urllib.request.Request("https://api.soracom.io/v1/subscribers/440525060011020/data?sort=desc&limit=1", headers=headers)
    with urllib.request.urlopen(req) as res:
        resBody = res.read().decode("utf-8")
        #データをjsonから辞書型に変換
        datas = json.loads(resBody)

    for data in datas:
        #必要なデータを辞書型に変換
        payloads = json.loads(data['content'])
        decodedData = base64.b64decode(payloads['payload']).decode("utf-8")

    return decodedData
