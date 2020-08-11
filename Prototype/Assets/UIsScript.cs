using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;
using GoogleMobileAds.Api;
using UnityEngine.UI;
using System;

public class UIsScript : MonoBehaviour
{

    public GameObject UIs;
    public GameObject DieUI;
    public GameObject SettingsUI;
    private Vector3 position;
    public GameObject Player;
    private string App_ID = "ca-app-pub-7957919444188102~3213415803";
    private string Video_ID = "ca-app-pub-3940256099942544/5224354917";
    private RewardBasedVideoAd rewardBasedVideo;


    public void Start()
    {
        MobileAds.Initialize(App_ID);
        RequestRewardBasedVideo();
    }

    public void NextLevel()
    {
        SceneManager.LoadScene(2);
    }

    public void MainMenu()
    {
        SceneManager.LoadScene(0);
    }

    public void TryAgain()
    {
        SceneManager.LoadScene(1);
    }

    public void Retry()
    {

        Debug.Log("Retry");
        UIs.SetActive(true);
        DieUI.SetActive(false);
        Time.timeScale = 1;

        GameObject[] points = GameObject.FindGameObjectsWithTag("SavePoint");


        GameObject Ninja = GameObject.Find("Ninja");
        Character character = Ninja.GetComponent<Character>();

        position = points[character.SafePoint].gameObject.transform.position;
        Player.transform.position = position;
        character.Lives = 4;

        for (int i = 0; i < character.hearts.Length; i++)
        {
            character.hearts[i].gameObject.SetActive(true);
        }
        ShowVideoRewardAd();

    }

    public void Settings()
    {
        SettingsUI.SetActive(true);
        UIs.SetActive(false);
        Invoke("FreazeGame", 2.0f);

    }
    
    public void Continue()
    {
        SettingsUI.SetActive(false);
        Time.timeScale = 1;
        UIs.SetActive(true);

    }

    public void FreazeGame()
    {
        Time.timeScale = 0;
    }

    public void RequestRewardBasedVideo()
    {
        rewardBasedVideo = RewardBasedVideoAd.Instance;
        AdRequest request = new AdRequest.Builder().Build();
        this.rewardBasedVideo.LoadAd(request, Video_ID);
    }

    public void ShowVideoRewardAd()
    {
        if (rewardBasedVideo.IsLoaded())
        {
            rewardBasedVideo.Show();
        }
    }

    public void HandleOnAdLoaded(object sender, EventArgs args)
    {
        Debug.Log("Qwerty");
    }

    public void HandleOnAdFailedToLoad(object sender, AdFailedToLoadEventArgs args)
    {
        MonoBehaviour.print("HandleFailedToReceiveAd event received with message: "
                            + args.Message);
    }

    public void HandleOnAdOpened(object sender, EventArgs args)
    {
        MonoBehaviour.print("HandleAdOpened event received");
    }

    public void HandleOnAdClosed(object sender, EventArgs args)
    {
        MonoBehaviour.print("HandleAdClosed event received");
    }

    public void HandleOnAdLeavingApplication(object sender, EventArgs args)
    {
        MonoBehaviour.print("HandleAdLeavingApplication event received");
    }

}
