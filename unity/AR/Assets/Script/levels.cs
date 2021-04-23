using Default;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

public class levels : MonoBehaviour
{

    [Header("Кнопки")]
    public Button BtnExit;
    public Button BtnReload;
    public Button BtnStart;

    [Header("")]
    public GameObject ImageReload;

 
    private PostStruct response;
    private string url = "https://chibiherbie.pythonanywhere.com/api/game";
    private int IdScene = 0;
    private int[] levelId;

    // Start is called before the first frame update
    void Start()
    {   
        levelId = new int[] {3, 4, 5, 6, 7};
        StartCoroutine(Get());
        BtnStart.interactable = false;
    }

    // Update is called once per frame
    void Update()
    {
        if (response.user_id == "")
        {
            ImageReload.SetActive(true);
        }
        else
        {
            ImageReload.SetActive(false);
        }
    }

    public void Reload()
    {
        Debug.Log("RELOAD");

        ImageReload.SetActive(true);
        response.user_id = "";

        StartCoroutine(Get());
    }

    public IEnumerator Get()
    {
        Debug.Log("LOAD API");

        UnityWebRequest request = UnityWebRequest.Get(url);

        yield return request.SendWebRequest();
        response = JsonUtility.FromJson<PostStruct>(request.downloadHandler.text);

        Debug.Log(response.user_id);

        if (response.level != 0)
        {
            IdScene = response.level - 1;
            BtnStart.interactable = true;
        }
        else
        {
            BtnStart.interactable = false;
        }
    }

    public void StartLevel()
    {
        StartCoroutine(AsyncLoad());
        ImageReload.SetActive(true);

        //SceneManager.LoadScene(levelId[IdScene]);
    }

    public void Exit()
    {   
        Application.Quit();
    }

    IEnumerator AsyncLoad()
    {
        AsyncOperation operation = SceneManager.LoadSceneAsync(levelId[IdScene]);
        yield return null;
    }
}
