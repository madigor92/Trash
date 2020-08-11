using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SavePoint : MonoBehaviour
{

    Collider2D m_Collider;

    void OnTriggerEnter2D(Collider2D other)
    {

        if (other.tag == "Player")
        {
            GameObject Ninja = GameObject.Find("Ninja");
            Character character = Ninja.GetComponent<Character>();
            character.SafePoint += 1;
            m_Collider = GetComponent<BoxCollider2D>();
            m_Collider.isTrigger = false;
            m_Collider.enabled = false;


        }
    }


}
