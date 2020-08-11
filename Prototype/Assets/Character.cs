using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityStandardAssets.CrossPlatformInput;

public class Character : MonoBehaviour
{
    private Rigidbody2D rb;
    private Animator anim;
    private float moveSpeed;
    private float dirX;
    private bool facingRight = true;
    private Vector3 localScale;
    public Transform barrel;
    public Rigidbody2D bullet;
    public float bulletSpeed = 500f;
    public Transform FireBall;
    public GameObject Heart;
    public int Lives = 4;

    private float lockPos = 0f;
    public GameObject CompleteLevelUI;
    public GameObject UIs;
    public GameObject DieUI;
    public int SafePoint = -1;
    public GameObject[] hearts;

    private void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
        localScale = transform.localScale;
        moveSpeed = 5f;
        hearts = GameObject.FindGameObjectsWithTag("Heart");

    }

    private void Update()
    {


        float a = Mathf.Round(rb.velocity.y * 1000f) / 1000f;
        dirX = CrossPlatformInputManager.GetAxis("Horizontal") * moveSpeed;


        if (CrossPlatformInputManager.GetButtonDown("Jump") && a == 0f)
        {
            rb.AddForce(Vector2.up * 500f);
        }


        if (CrossPlatformInputManager.GetButtonDown("Fire"))
            Fire();

        if (Mathf.Abs(dirX) > 0f && a == 0f)
        {
            anim.SetBool("isRunning", true);

        }
        else
        {
            anim.SetBool("isRunning", false);

        }

        if (a < 1f &&  a > -1f)
        {
            anim.SetBool("isJumping", false);


        }
        if (a > 1f || a < -1f)
        {
            anim.SetBool("isJumping", true);

        }

        if (Lives == 0) {
            Die();
        }



    }

    private void FixedUpdate()
    {
        rb.velocity = new Vector2(dirX, rb.velocity.y);
        transform.rotation = Quaternion.Euler(transform.rotation.eulerAngles.x, lockPos, lockPos);
    }

    private void LateUpdate()
    {
        if (dirX > 0)
            facingRight = true;
        else if (dirX < 0)
            facingRight = false;

        if (((facingRight) && (localScale.x < 0)) || ((!facingRight) && (localScale.x > 0)))
            localScale.x *= -1;

        transform.localScale = localScale;
    }

    void Fire()
    {
        var firedBullet = Instantiate(bullet, barrel.position, FireBall.rotation);
        firedBullet.AddForce(barrel.up * bulletSpeed);

    }
    void OnCollisionEnter2D(Collision2D collision)
    {

        if (collision.gameObject.tag == "theobjectToIgnore")
        {
           
            hearts[Lives - 1].gameObject.SetActive(false);
            Lives -= 1;
        }

        if (collision.gameObject.tag == "Finish")
        {
            FinishLevel();
        }
        if (collision.gameObject.tag == "Spike")
        {
            Die();
            Debug.Log("Spike");
        }

        if (collision.gameObject.tag == "Platform")
        {
            transform.Translate(Vector3.right * Time.deltaTime * 5f);
            Debug.Log("Collision");
        }

        if (collision.gameObject.tag == "Healer")
        {
            Lives += 1;
            hearts[Lives - 1].gameObject.SetActive(true);
            Destroy(collision.gameObject);
        }
    }



    public void FinishLevel()
    {
        CompleteLevelUI.SetActive(true);
        UIs.SetActive(false);
    }

    public void Die()
    {
        DieUI.SetActive(true);
        UIs.SetActive(false);
    }

}

