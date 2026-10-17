using UnityEngine;

[DefaultExecutionOrder(-1000)]
public class Game : MonoBehaviour
{
    public static Game Instance { get; private set; }

    private void Awake()
    {
        Instance = this;
        QualitySettings.vSyncCount = 0;
        Application.targetFrameRate = GameClock.TargetFps;
        Time.fixedDeltaTime = 1f / GameClock.TargetFps;
    }

    private void FixedUpdate()
    {
        GameClock.Tick();
    }
}