using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class FireBall : MonoBehaviour

{
    [SerializeField]
    float destroyTime = 2f;
    private SpriteRenderer mySpriteRenderer;
    private float startY;
    private float currentY;


    void Start()
    {
        startY = transform.position.x;
        mySpriteRenderer = GetComponent<SpriteRenderer>();
        Destroy(gameObject, destroyTime);

    }

    void Update()
    {
        currentY = transform.position.x;
        if (currentY > startY)
            mySpriteRenderer.flipX = false;
        if (currentY < startY)
            mySpriteRenderer.flipX = true;
    }


     void OnCollisionEnter2D(Collision2D collision)
     {
  
        if (collision.gameObject.tag == "Obstacle" || collision.gameObject.tag == "Platform" || collision.gameObject.tag == "Player")
        {
            Destroy(gameObject);
        }
    }

    void OnEnable()
    {
        GameObject[] otherObjects = GameObject.FindGameObjectsWithTag("theobjectToIgnore");
        foreach (GameObject obj in otherObjects)
        {
            Physics2D.IgnoreCollision(obj.GetComponent<Collider2D>(), GetComponent<Collider2D>());
        }
    }
}

