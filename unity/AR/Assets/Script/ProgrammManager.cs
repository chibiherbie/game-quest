using Default;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using UnityEngine.SceneManagement;
using UnityEngine.UI;
using UnityEngine.XR.ARFoundation;
using UnityEngine.XR.ARSubsystems;

public class ProgrammManager : MonoBehaviour
{

    [Header("Set PlaneMarker for ground")]
    [SerializeField] private GameObject PlaneMarkerPrefab;

    private ARRaycastManager ARRaycastManagerScript;

    private Vector2 TouchPosition;

    public GameObject ObjectToSpawn;

    public Text timerText;

    [Header("Set text for timer")]
    private float timeStart = 60;
    private PostStruct response;
    private string url = "https://chibiherbie.pythonanywhere.com/api/game";

    void Start()
    {
        StartCoroutine(Get());

        ARRaycastManagerScript = FindObjectOfType<ARRaycastManager>();

        PlaneMarkerPrefab.SetActive(false);
    }

    // Update is called once per frame
    void Update()
    {
        SetMarker();
        timeStart -= Time.deltaTime;
        timerText.text = Mathf.Round(timeStart).ToString();

        Debug.Log(timeStart);


        if (Mathf.Round(timeStart) == 0)
        {
            StartCoroutine(AsyncLoad());
        }
    }


    void SetMarker()
    {
        List<ARRaycastHit> hits = new List<ARRaycastHit>();

        ARRaycastManagerScript.Raycast(new Vector2(Screen.width / 2, Screen.height / 2), hits, TrackableType.Planes);

        // еслси есть пересечения, показываем маркер
        if (hits.Count > 0)
        {
            PlaneMarkerPrefab.transform.position = hits[0].pose.position;
            PlaneMarkerPrefab.SetActive(true);
        }

        // ставим сцену на точку
        if (Input.touchCount > 0 && Input.GetTouch(0).phase == TouchPhase.Began)
        {
            Instantiate(ObjectToSpawn, hits[0].pose.position, ObjectToSpawn.transform.rotation);
        }
    }

    public IEnumerator Get()
    {
        Debug.Log("LOAD API");

        UnityWebRequest request = UnityWebRequest.Get(url);

        yield return request.SendWebRequest();
        response = JsonUtility.FromJson<PostStruct>(request.downloadHandler.text);

        Debug.Log(response.time);

        timeStart = response.time;
        timerText.text = timeStart.ToString();
    }

    IEnumerator AsyncLoad()
    {
        AsyncOperation operation = SceneManager.LoadSceneAsync(2);
        yield return null;
    }
}
