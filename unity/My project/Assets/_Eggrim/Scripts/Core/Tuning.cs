using UnityEngine;
public class Tuning : MonoBehaviour
{
    public static int ScreenW = 200;
    public static int ScreenH = 200;

    public static int DisplayScale = 5;

    public static int WidthPixels = ScreenW * DisplayScale;
    public static int HeightPixels = ScreenH * DisplayScale;

    private const int Tile = 8;
    private const int BodyOffsetY = 8;
    private const int FeetRadius = 2;
}