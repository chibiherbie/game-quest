using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using System.IO;
using System.Linq;
using Default;
using System;
using System.Text;

namespace API
{
    public class HttpRequest : MonoBehaviour
    {

        [SerializeField] public string url;

        public PostStruct itemJson;
        private PostStruct response;
        public int Id;

        private string savePath;

        public void Start()
        {
            Debug.Log("START");

            StartCoroutine(SendRequest());
            // StartCoroutine(PostRequest());
        }

        public IEnumerator SendRequest()
        {
            UnityWebRequest request = UnityWebRequest.Get(this.url);

            yield return request.SendWebRequest();
            Debug.Log("TEXT: " + request.downloadHandler.text);

            response = JsonUtility.FromJson<PostStruct>(request.downloadHandler.text);

            LoadField();
            Debug.Log("JSON: " + itemJson.user_id);
            Debug.Log("API: " + response.user_id);


            if (itemJson.user_id != response.user_id)
            {
                Id = 1;
            }
            else
            {
                Id = 2;
            }
        }

        public void GetApi()
        {
            StartCoroutine(Get());
        }

        private IEnumerator Get()
        {
            Debug.Log("LOAD");
            UnityWebRequest request = UnityWebRequest.Get("https://chibiherbie.pythonanywhere.com/api/game");


            yield return request.SendWebRequest();
            response = JsonUtility.FromJson<PostStruct>(request.downloadHandler.text);
        }

        public IEnumerator PostRequest()
        {
            WWWForm formData = new WWWForm();

            PostStruct post = new PostStruct()
            {
                user_id = "qwe",
                time = 10,
                level = 1

            };

            string json = JsonUtility.ToJson(post);

            UnityWebRequest request = UnityWebRequest.Post(this.url, formData);

            byte[] postbytes = Encoding.UTF8.GetBytes(json);

            UploadHandler uploadHandler = new UploadHandlerRaw(postbytes);

            request.uploadHandler = uploadHandler;

            request.SetRequestHeader("Content-Type", "application/json; charset=UTF-8");

            yield return request.SendWebRequest();  
        }

        public void LoadField()
        {
            Debug.Log("PATH: " + Application.streamingAssetsPath + "  " + Application.dataPath + "   " + Application.persistentDataPath);

#if UNITY_ANDROID && !UNITY_EDITOR
        savePath = Path.Combine(Application.persistentDataPath, "config.json");
#else
        savePath = Path.Combine(Application.dataPath, "config.json");
#endif

            string json = File.ReadAllText(savePath);

            itemJson = JsonUtility.FromJson<PostStruct>(json);
            Debug.Log("---PATH ON LOAD: " + savePath);
        }

        public void SaveField(string IDUser)
        {
            try
            {
                string conn = Path.Combine(Application.dataPath, "config.json");

                Debug.Log(conn + IDUser);

                string[] arr = { "asd", "asd" };
                PostStruct file = new PostStruct
                {
                    user_id = IDUser,
                    time = 0,
                    level = 0,
                    items = arr
                };

                

                WWW dbPath = new WWW(conn);

                //File.WriteAllText(conn, JsonUtility.ToJson(file, true));
            }
            catch (Exception e)
            {
                Debug.Log(e);
            }
        }
    }
}
