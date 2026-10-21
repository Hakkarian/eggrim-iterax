using UnityEngine;
using UnityEditor;

public class HeroFrontRig
{
    const string Folder = "Assets/_Eggrim/Art/Hero/Front";
    const float CanvasWidth = 24f;
    const float CanvasHeight = 48f;

    class Part
    {
        public string Name;
        public Rect OnCanvas;
    }

    static readonly Part[] PartsBackToFront =
    {
        new Part { Name = "leg_right", OnCanvas = new Rect(7, 33, 5, 15) },
        new Part { Name = "leg_left", OnCanvas = new Rect(12, 34, 5, 14) },
        new Part { Name = "body", OnCanvas = new Rect(6, 17, 12, 19) },
        new Part { Name = "hand_right", OnCanvas = new Rect(0, 17, 11, 19) },
        new Part { Name = "hand_left", OnCanvas = new Rect(14, 17, 9, 18) },
        new Part { Name = "head", OnCanvas = new Rect(1, 2, 22, 18) },
    };

    static readonly Vector2 CanvasBottomMiddle = new Vector2(CanvasWidth / 2f, CanvasHeight);

    [MenuItem("Eggrim/Build Front Rig")]
    public static void Build()
    {
        foreach (Part part in PartsBackToFront)
        {
            SpriteImportPreset.Apply($"{Folder}/readmey_front_{part.Name}.png");
        }

        GameObject hero = new GameObject("Hero");
        hero.AddComponent<Hero>();

        int drawOrder = 0;
        foreach (Part part in PartsBackToFront)
        {
            AddPartSprite(hero, part, drawOrder);
            drawOrder += 1;
        }

        Undo.RegisterCreatedObjectUndo(hero, "Build Front Rig");
        Selection.activeGameObject = hero;
    }

    static void AddPartSprite(GameObject hero, Part part, int drawOrder)
    {
        GameObject partSprite = new GameObject(part.Name);
        partSprite.transform.SetParent(hero.transform);
        partSprite.transform.localPosition = CenterAboveGround(part.OnCanvas);
        SpriteRenderer sprite = partSprite.AddComponent<SpriteRenderer>();
        sprite.sprite = AssetDatabase.LoadAssetAtPath<Sprite>($"{Folder}/readmey_front_{part.Name}.png");
        sprite.sortingOrder = drawOrder;
    }

    static Vector3 CenterAboveGround(Rect part)
    {
        float sideways = part.center.x - CanvasBottomMiddle.x;
        float up = CanvasBottomMiddle.y - part.center.y;
        return new Vector3(sideways, up, 0f);
    }
}