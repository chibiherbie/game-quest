using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using API;
using Default;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;
using System.IO;
using System;

public class Menu : MonoBehaviour
{

    public string theName;
    public GameObject InputFields;
    public GameObject textLoad;
    public GameObject textError;
    private PostStruct response;
    private HttpRequest con;
    private string savePath;


    // Start is called before the first frame update
    void Start()
    {
        textLoad.SetActive(false);
        textError.SetActive(false);
        theName = "";

        StartCoroutine(Get());
    }

    // Update is called once per frame
    void Update()
    {
        if (response.user_id != theName && theName != "")
        {

            Debug.Log(response.user_id);
            if (response.user_id == "")
            {
                textLoad.SetActive(true);
                textError.SetActive(false);
            }
            else {
                textError.SetActive(true);
                textLoad.SetActive(false);
            }
            

        }
        else if (response.user_id == theName && theName != "") {


            Debug.Log("«¿œ»—‹ ¬ ‘¿…À" + response.user_id);
            SaveField(response.user_id);

            textError.SetActive(false);
            textLoad.GetComponent<Text>().text = "”ÒÔÂ¯ÌÓ";

            SceneManager.LoadScene(2);
        }
    }


    public void CheckId()
    {
        Debug.Log("SEND");
        response.user_id = "";
        textError.SetActive(false);

        theName = InputFields.GetComponent<Text>().text;

        StartCoroutine(Get());

        Debug.Log(response.user_id);
    }

    public IEnumerator Get()
    {
        Debug.Log("LOAD");
        UnityWebRequest request = UnityWebRequest.Get("https://chibiherbie.pythonanywhere.com/gg");


        yield return request.SendWebRequest();
        response = JsonUtility.FromJson<PostStruct>(request.downloadHandler.text);
        Debug.Log(response.user_id);
    }

    public void SaveField(string ID)
    {
        try
        {   
            Debug.Log("--- PATH ON SAVE: " + savePath + ID);

            string[] arr = { "asd", "asd" };
            PostStruct file = new PostStruct
            {
                user_id = ID,
                time = 0,
                level = 0,
                items = arr
            };

            //itemJson.user_id = ID;

            //WWW dbPath = new WWW(conn);

            File.WriteAllText(savePath, JsonUtility.ToJson(file, true));
        }
        catch (Exception e)
        {
            Debug.Log(e);
        }
    }

    private void Awake()
    {

#if UNITY_ANDROID && !UNITY_EDITOR
        savePath = Path.Combine(Application.persistentDataPath, "config.json");
#else
        savePath = Path.Combine(Application.dataPath, "config.json");
#endif

    }
}
