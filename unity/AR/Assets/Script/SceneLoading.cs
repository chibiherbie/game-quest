using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.SceneManagement;
using API;
using System.IO;

public class SceneLoading : MonoBehaviour
{
    public Image loadingImage;
    public int SceneID;

    public HttpRequest load;

    float progress = 0;

    public GameObject TextInfo;

    void Start()
    {
        load.Start();
        SceneID = load.Id;
        Debug.Log(SceneID);

        TextInfo.SetActive(false);
    }

    private void Update()
    {
        if (SceneID != 0)
        {               
            StartCoroutine(AsyncLoad());
        }
     
        else
        {
            Debug.Log(SceneID);
            SceneID = load.Id;

            if (progress < 0.3)
            {
                progress += 0.003f;
                loadingImage.fillAmount = progress;
            }
        }

        switch (Application.internetReachability)
        {
            case NetworkReachability.ReachableViaLocalAreaNetwork:
                Debug.Log("Internet connection");
                TextInfo.SetActive(false);
                load.Start();
                break;

            case NetworkReachability.ReachableViaCarrierDataNetwork:
                Debug.Log("Internet connection");
                TextInfo.SetActive(false);
                load.Start();
                break;

            default:
                Debug.Log("No internet connection");
                TextInfo.GetComponent<Text>().text = "No internet";
                TextInfo.SetActive(true);
                break;
        }
    }

    IEnumerator AsyncLoad()
    {
        AsyncOperation operation = SceneManager.LoadSceneAsync(SceneID);
    
        while (!operation.isDone)
        {   
            if (operation.progress > progress)
            {
                progress = operation.progress / 0.9f;
            }

            loadingImage.fillAmount = progress;
            yield return null;

        }
    }
}
