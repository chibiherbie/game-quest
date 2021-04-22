using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using API;
using Default;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;

public class Menu : MonoBehaviour
{

    public string theName;
    public GameObject InputFields;
    public GameObject textLoad;
    public GameObject textError;
    private PostStruct response;
    private HttpRequest con;


    // Start is called before the first frame update
    void Start()
    {
        textLoad.SetActive(false);
        textError.SetActive(false);
        theName = "";
    }

    // Update is called once per frame
    void Update()
    {
        if (response.user_id != theName && theName != "")
        {
            Debug.Log("«¿√–”« ¿");
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
        else if (response.user_id == theName) {
            textError.SetActive(false);
            textLoad.GetComponent<Text>().text = "”ÒÔÂ¯ÌÓ";
            SceneManager.LoadScene(3);  
        }
    }


    public void CheckId()
    {
        Debug.Log("SEND");
        response.user_id = "";

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
}
