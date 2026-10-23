using UnityEngine;
using UnityEditor;
using System.IO;

public class ArenaBuilder
{
    const string Folder = "Assets/_Eggrim/Art/Arena";
    const string Png = Folder + "/arena_checker.png";
    const int Size = 2000;
    const int Cell = 100;
    static readonly Color Light = new Color(0.87f, 0.80f, 0.64f);
    static readonly Color Dark = new Color(0.75f, 0.67f, 0.50f);

    [MenuItem("Eggrim/Build Arena")]
    public static void Build()
    {
        AssetDatabase.CreateFolder("Assets/_Eggrim/Art", "Arena");
        string path = SaveChecker();
        AssetDatabase.Refresh();
        SpriteImportPreset.Apply(path);

        GameObject arena = new GameObject("Arena");
        SpriteRenderer sprite = arena.AddComponent<SpriteRenderer>();
        sprite.sprite = AssetDatabase.LoadAssetAtPath<Sprite>(path);
        sprite.sortingOrder = -1;
        Undo.RegisterCreatedObjectUndo(arena, "Build Arena");
        Selection.activeGameObject = arena;
        AimCamera();
    }

    static void AimCamera()
    {
        Camera camera = Camera.main;
        Undo.RecordObject(camera, "Build Arena");
        Undo.RecordObject(camera.transform, "Build Arena");
        camera.orthographic = true;
        camera.orthographicSize = 600f;
    }

    static string SaveChecker()
    {
        Texture2D texture = new Texture2D(Size, Size, TextureFormat.RGBA32, false);
        for (int y = 0; y < Size; y++)
        {
            for (int x = 0; x < Size; x++)
            {
                bool even = ((x / Cell) + (y / Cell)) % 2 == 0;
                texture.SetPixel(x, y, even ? Light : Dark);
            }
        }
        texture.Apply();
        File.WriteAllBytes(Png, texture.EncodeToPNG());
        return Png;
    }
}