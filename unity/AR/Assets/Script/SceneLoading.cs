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

    public API.HttpRequest load;

    void Start()
    {
        load.Start();
        SceneID = load.Id;
        Debug.Log(SceneID);

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
        }
    }

    IEnumerator AsyncLoad()
    {
        AsyncOperation operation = SceneManager.LoadSceneAsync(SceneID);
    
        while (!operation.isDone)
        {
            float progress = operation.progress / 0.9f;
            loadingImage.fillAmount = progress;
            yield return null;
        }
    }
}
