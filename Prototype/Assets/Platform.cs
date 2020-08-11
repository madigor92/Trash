using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Platform : MonoBehaviour
{
    private float scale = 5f;
    public GameObject player;
    public bool Movement = false;


    void Update()
    {

        if (transform.position.x >  44f)
        {
            scale = -5f;
        }
        if (transform.position.x < 23.826f)
        {
            scale = 5f;
        }
        transform.Translate(Vector3.right * Time.deltaTime * scale);

        if (Movement)
        {
            player.transform.Translate(Vector3.right * Time.deltaTime * scale);
        }


    }

    void OnCollisionEnter2D(Collision2D other)
    {
        if (other.gameObject.CompareTag("Player"))
        {
            Movement = true;
        }
    }

    void OnCollisionExit2D(Collision2D other)
    {
        if (other.gameObject.CompareTag("Player"))
        {
            Movement = false;
        }
    }

}
