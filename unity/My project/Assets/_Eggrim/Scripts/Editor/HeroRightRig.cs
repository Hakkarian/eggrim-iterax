using UnityEngine;
using UnityEditor;

public class HeroRightRig
{
    const string Folder = "Assets/_Eggrim/Art/Hero/Right";
    const float CanvasWidth = 26f;
    const float CanvasHeight = 48f;

    class Part
    {
        public string Name;
        public Rect OnCanvas;
    }

    static readonly Part[] PartsBackToFront =
    {
        new Part { Name = "leg_back", OnCanvas = new Rect(5, 32, 9, 16) },
        new Part { Name = "leg_front", OnCanvas = new Rect(12, 32, 10, 16) },
        new Part { Name = "body", OnCanvas = new Rect(3, 17, 18, 19) },
        new Part { Name = "head", OnCanvas = new Rect(1, 2, 20, 20) },
        new Part { Name = "hand", OnCanvas = new Rect(8, 17, 8, 19) },
    };

    static readonly Vector2 CanvasBottomMiddle = new Vector2(CanvasWidth / 2f, CanvasHeight);

    [MenuItem("Eggrim/Build Right Rig")]
    public static void Build()
    {
        foreach (Part part in PartsBackToFront)
        {
            SpriteImportPreset.Apply($"{Folder}/readmey_right_{part.Name}.png");
        }

        GameObject hero = new GameObject("HeroRight");

        int drawOrder = 0;
        foreach (Part part in PartsBackToFront)
        {
            AddPartSprite(hero, part, drawOrder);
            drawOrder += 1;
        }

        Undo.RegisterCreatedObjectUndo(hero, "Build Right Rig");
        Selection.activeGameObject = hero;
    }

    static void AddPartSprite(GameObject hero, Part part, int drawOrder)
    {
        GameObject partSprite = new GameObject(part.Name);
        partSprite.transform.SetParent(hero.transform);
        partSprite.transform.localPosition = CenterAboveGround(part.OnCanvas);
        SpriteRenderer sprite = partSprite.AddComponent<SpriteRenderer>();
        sprite.sprite = AssetDatabase.LoadAssetAtPath<Sprite>($"{Folder}/readmey_right_{part.Name}.png");
        sprite.sortingOrder = drawOrder;
    }

    static Vector3 CenterAboveGround(Rect part)
    {
        float sideways = part.center.x - CanvasBottomMiddle.x;
        float up = CanvasBottomMiddle.y - part.center.y;
        return new Vector3(sideways, up, 0f);
    }
}