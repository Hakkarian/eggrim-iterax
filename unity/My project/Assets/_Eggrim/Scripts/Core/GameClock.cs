using UnityEngine;

public class GameClock {

    public static int TargetFps = 60;
    
    public static int Frame { get; private set; }

    public static void Tick()
    {
        Frame++;
    }

    public static void Reset()
    {
        Frame = 0;
    }

}