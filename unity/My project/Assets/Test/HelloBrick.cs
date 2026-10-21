using UnityEngine;

public class HelloBrick : MonoBehaviour
{
    void Start()
    {
        Debug.Log("greetings,", this);
        GetComponent<SpriteRenderer>().color = new Color(1f, 0f, 0f, 1f);
    }
}