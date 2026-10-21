using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Rigidbody2D))]
public class Hero : MonoBehaviour
{
    [SerializeField] float moveSpeed = 30f;

    Rigidbody2D body;

    void Awake()
    {
        body = GetComponent<Rigidbody2D>();
        body.gravityScale = 0f;
    }

    void FixedUpdate()
    {
        body.linearVelocity = ReadDirection() * moveSpeed;
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