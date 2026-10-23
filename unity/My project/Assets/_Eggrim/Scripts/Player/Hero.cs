using UnityEngine;
using UnityEngine.InputSystem;

[RequireComponent(typeof(Rigidbody2D))]
public class Hero : MonoBehaviour
{
    [SerializeField] GameObject facingFront;
    [SerializeField] GameObject facingBack;
    [SerializeField] GameObject facingLeft;
    [SerializeField] GameObject facingRight;
    [SerializeField] float moveSpeed = 30f;

    Rigidbody2D body;

    void Awake()
    {
        body = GetComponent<Rigidbody2D>();
        body.gravityScale = 0f;
        body.interpolation = RigidbodyInterpolation2D.Interpolate;
    }

    void FixedUpdate()
    {
        Vector2 direction = ReadDirection();
        body.linearVelocity = direction * moveSpeed;
        FaceMovement(direction);
    }

    void FaceMovement(Vector2 direction)
    {
        GameObject facing = facingFront;
        if (direction.x < 0) facing = facingLeft;
        else if (direction.x > 0) facing = facingRight;
        else if (direction.y > 0) facing = facingBack;

        facingFront.SetActive(facing == facingFront);
        facingBack.SetActive(facing == facingBack);
        facingLeft.SetActive(facing == facingLeft);
        facingRight.SetActive(facing == facingRight);
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