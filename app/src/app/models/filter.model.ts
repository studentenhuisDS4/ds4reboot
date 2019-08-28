import 'reflect-metadata';

export const META_KEY = Symbol('propertyMetadata');

export interface Filter {
    serialize(filter: any): void;
}

export interface IFilterMeta {
    name: string;
}

export class BaseFilter implements Filter {
    serialize(): string {
        let query = '';
        Object.keys(this).forEach(key => {
            const meta = Reflect.getMetadata(META_KEY, this)[key] as IFilterMeta;
            if (this[key]) {
                if (meta && meta.name) {
                    query += meta.name + '=' + this[key] + '&';
                } else {
                    query += key + '=' + this[key] + '&';
                }
            }
        });
        return `?${query.slice(0, -1)}`;
    }
}

// https://blog.wizardsoftheweb.pro/typescript-decorators-property-decorators/
export function mapping(updates: IFilterMeta) {
    return (target: any, propertyKey: string | symbol) => {
        // Pull the existing metadata or create an empty object
        const allMetadata: IFilterMeta = (
            Reflect.getMetadata(META_KEY, target)
            ||
            {}
        );
        // Ensure allMetadata has propertyKey
        allMetadata[propertyKey] = (
            allMetadata[propertyKey]
            ||
            {}
        );
        // Update the metadata with anything from updates
        for (const key of Reflect.ownKeys(updates)) {
            allMetadata[propertyKey][key] = updates[key];
        }
        // Update the metadata
        Reflect.defineMetadata(
            META_KEY,
            allMetadata,
            target,
        );
    };
}
