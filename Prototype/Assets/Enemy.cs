using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Enemy : MonoBehaviour
{
    private float rate = 2.0F;
    public Rigidbody2D bullet;
    public float bulletSpeed = 500f;
    public Transform barrel;
    public Transform FireBall;
    public GameObject Character;
    private SpriteRenderer mySpriteRenderer;
    private Vector3 localScale;
    private bool facingLeft;
    private bool a = true;
    private float lockPos = 0f;
    public int Lives = 3;

    public void Start()
    {
        InvokeRepeating("Shoot", rate, rate);
        mySpriteRenderer = GetComponent<SpriteRenderer>();
        localScale = transform.localScale;
    }

    public void Shoot()
    {
        var firedBullet = Instantiate(bullet, barrel.position, FireBall.rotation);
        firedBullet.AddForce(barrel.up * bulletSpeed);
    }

    public void LateUpdate()
    {
        transform.rotation = Quaternion.Euler(transform.rotation.eulerAngles.x, lockPos, lockPos);
        if (transform.position.x > Character.transform.position.x)
            facingLeft = true;
        else if (transform.position.x < Character.transform.position.x)
            facingLeft = false;


        if (a != facingLeft)
            localScale.x *= -1;
     
        transform.localScale = localScale;
        a = facingLeft;

        if (Lives == 0)
        {
            Destroy(gameObject);
        }
    }

    void OnCollisionEnter2D(Collision2D collision)
    {

        if (collision.gameObject.tag == "theobjectToIgnore")
        {

            Lives -= 1;
        }
        if (collision.gameObject.tag == "Obstacle")
        {
            float b = collision.collider.gameObject.transform.position.y - transform.position.y;
            if (b > 1.5f)
            {
                Lives -= 1;
            }

        }
    }
}
