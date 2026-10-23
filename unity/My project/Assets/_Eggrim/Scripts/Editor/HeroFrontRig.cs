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
        GameObject front = new GameObject("Front");
        front.transform.SetParent(hero.transform);


        int drawOrder = 0;
        foreach (Part part in PartsBackToFront)
        {
            SpritesHelper.AddPartSprite(front, part.Name, $"{Folder}/readmey_front_{part.Name}.png", part.OnCanvas, drawOrder);
            drawOrder += 1;
        }

        SerializedObject heroState = new SerializedObject(hero.GetComponent<Hero>());
        heroState.FindProperty("facingFront").objectReferenceValue = front;
        heroState.ApplyModifiedProperties();

        Undo.RegisterCreatedObjectUndo(hero, "Build Front Rig");
        Selection.activeGameObject = hero;
    }
}