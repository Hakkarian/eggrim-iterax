using UnityEngine;
using UnityEngine.InputSystem;

public class Hero : MonoBehaviour
{
    [SerializeField] float moveSpeed = 30f;

    void Update()
    {
        Vector2 direction = ReadDirection();
        transform.position += (Vector3)(direction * moveSpeed * Time.deltaTime);
    }

    Vector2 ReadDirection()
    {
        float x = 0;
        float y = 0;
        if (Keyboard.current.dKey.isPressed) x += 1;
        if (Keyboard.current.aKey.isPressed) x -= 1;
        if (Keyboard.current.wKey.isPressed) y += 1;
        if (Keyboard.current.sKey.isPressed) y -= 1;
        return new Vector2(x, y);
    }
}