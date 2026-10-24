using UnityEngine;

public class HeroWalk : MonoBehaviour
{
    [SerializeField] GameObject[] parts;
    [SerializeField] SpriteRenderer run;
    [SerializeField] Sprite[] frames;
    [SerializeField] float frameRate = 8f;

    public void Step(Vector2 direction)
    {
        bool moving = direction != Vector2.zero;
        foreach (GameObject part in parts)
        {
            part.SetActive(!moving);
        }
        run.gameObject.SetActive(moving);
        run.sprite = frames[(int)(Time.time * frameRate) % frames.Length];
    }
}